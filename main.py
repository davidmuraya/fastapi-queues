# main.py (FastAPI)
from celery.result import AsyncResult
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session

from celery_config import celery_app
from database.connection import get_db
from database.utils.celery_crud import get_task_id
from tasks import add, divide

app = FastAPI()


@app.post("/add")
async def add_numbers(x: int, y: int):
    username = "test_user"  # Replace with actual username logic
    task = add.apply_async((x, y), {"username": username})
    return {"task_id": task.id, "message": "Task queued successfully!"}


@app.post("/divide")
async def divide_numbers(x: int, y: int):
    task = divide.delay(x, y)

    return {"task_id": task.id, "message": "Task queued successfully!"}


@app.get("/result/{task_id}")
async def get_result(task_id: str, db: Session = Depends(get_db)):
    """
    Get the result of a task by its task_id.
    Raises HTTPException(404) if not found, or 500 on DB errors.
    """
    # 0) Check if the task ID is valid
    task_id_check_response = await get_task_id(db, task_id)

    if task_id_check_response == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task ID not found.")

    res = AsyncResult(task_id, app=celery_app)

    # 1) Still running or retrying
    if res.state in ("PENDING", "RETRY"):
        return {"status": res.state, "task_id": task_id, "result": None}

    # 2) Errored out
    if res.state == "FAILURE":
        # .traceback gives you the full traceback string
        tb = res.traceback or "No traceback available"
        # .result will be the Exception instance
        exc = res.result
        # You can choose to hide the full tb in production
        raise HTTPException(
            status_code=500,
            detail={
                "status": res.state,
                "error": repr(exc),
                "result": None,
                "traceback": tb.splitlines()[-5:],  # last 5 lines
            },
        )

    # 3) Success
    # propagate=False means .get() won't re-raise if something weird happened
    value = res.get(propagate=False)
    username = value.get("username", None) if isinstance(value, dict) else None
    result = value.get("result", None) if isinstance(value, dict) else value

    return {"status": res.state, "result": result, "task_id": task_id, "username": username}

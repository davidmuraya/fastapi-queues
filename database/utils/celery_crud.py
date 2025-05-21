import logging

from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlmodel import Session


async def get_task_id(db: Session, task_id: str) -> int:
    """
    Fetch a celery_taskmeta row by task_id.
    Raises HTTPException(404) if not found, or 500 on DB errors.
    """
    id = 0
    try:
        stmt = text("SELECT task_id FROM celery_taskmeta WHERE task_id = :task_id")
        scalar = db.scalars(stmt, params={"task_id": task_id}).one_or_none()

        if scalar is not None:
            id = scalar

    except DBAPIError as e:
        # log e if you have a logger
        logging.critical(f"Database error: {e!r}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error while fetching task.")

    return id

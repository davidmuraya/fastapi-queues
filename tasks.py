# tasks.py
import logging
import time
from typing import Optional

import httpx
from httpx import HTTPStatusError, RequestError

from celery_config import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def long_call(self, url: str):
    try:
        res = httpx.get(url, timeout=180)  # 3 minutes
        res.raise_for_status()
        return res.json()
    except RequestError as exc:
        # network problem: retry
        raise self.retry(exc=exc)
    except HTTPStatusError as exc:
        logging.error(f"Request failed: {exc!r}")
        # bad HTTP status: probably not worth retrying
        raise


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60, name="add_task")
def add(self, x, y, username: Optional[str] = None):
    print(f"Adding {x} and {y}")
    self.update_state(state="PENDING", meta={"username": username})
    time.sleep(5)  # Simulate a long-running task
    result = x + y
    print(f"Result: {result}")
    return {"result": result, "username": username}


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def divide(self, x, y):
    print(f"Dividing {x} and {y}")
    try:
        result = x / y
        return result
    except Exception as exc:
        print(f"Error occurred: {exc}")

        raise self.retry(exc=exc)

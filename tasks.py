# tasks.py
import time

import httpx

from celery_config import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def long_call(self, url: str):
    try:
        res = httpx.get(url, timeout=180)  # 3-min timeout
        res.raise_for_status()
        return res.json()
    except Exception as exc:
        print(f"Error occurred: {exc}")
        # Only retry for connection errors
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def add(self, x, y):
    print(f"Adding {x} and {y}")
    time.sleep(5)  # Simulate a long-running task
    result = x + y
    print(f"Result: {result}")
    return result


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def divide(self, x, y):
    print(f"Dividing {x} and {y}")
    try:
        result = x / y
        return result
    except Exception as exc:
        print(f"Error occurred: {exc}")

        raise self.retry(exc=exc)

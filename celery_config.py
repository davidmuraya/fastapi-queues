from celery import Celery

from config import get_settings
from database.connection import DATABASE_URL

settings = get_settings()


# Celery Backend Configuration
CELERY_BACKEND = f"db+{DATABASE_URL}"

celery_app = Celery("worker", broker=settings.REDIS_BROKER_URL, backend=CELERY_BACKEND, include=["tasks"])

# Tell the Redis transport to use longer timeouts
celery_app.conf.update(
    broker_transport_options={
        # how long to wait for a socket connect (seconds)
        "socket_connect_timeout": 30,
        # how long to wait for any call (seconds)
        "socket_timeout": 300,
        # how long a task can stay invisible (for retries) (seconds)
        "visibility_timeout": 3600,
    },
    result_backend_transport_options={
        "socket_timeout": 300,
    },
)

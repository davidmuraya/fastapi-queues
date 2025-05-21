from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_BROKER_URL: str = Field(..., description="REDIS_BROKER_URL")
    CELERY_DB: str = Field(..., description="CELERY_DB")

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()

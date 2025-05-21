from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_settings

settings = get_settings()

# Local Celery Database Configuration
DATABASE_PATH = Path(settings.CELERY_DB)
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
CONNECT_ARGS = {"check_same_thread": False}


engine = create_engine(DATABASE_URL, echo=False, connect_args=CONNECT_ARGS)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI, Celery + Redis

A production-ready FastAPI project for managing background task queues using Celery and Redis. This project demonstrates how to offload long-running or resource-intensive tasks from your FastAPI API to asynchronous workers, enabling scalable and reliable background job execution. It includes queue management endpoints, example producer/consumer patterns, and a modular structure for easy extension.


## Features

- Asynchronous background task processing with Celery
- FastAPI endpoints to enqueue and monitor tasks
- Integration with Redis for robust, production-grade queue management
- Example producer/consumer patterns (e.g., addition, division tasks)
- Task status and result retrieval via API
- Modular codebase with clear separation of API, tasks, and configuration
- Optional in-memory queue support for development/testing
- Windows and Linux compatibility

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Celery
- Redis (for production queue backend)
- SQLModel (for database interactions)

## Installation

```bash
git clone https://github.com/davidmuraya/fastapi-queues.git
cd fastapi-queues
pip install -r requirements.txt
```

Ensure you have Redis installed and running on your machine.

Create a `.env` file in the root directory and add the following lines:

```bash
REDIS_BROKER_URL=redis://localhost:6379/0
CELERY_DB=database/celery.db
```

## Usage

### Running the API

```bash
uvicorn main:app --reload --port 5000
```

#### Celery Worker
```bash
celery -A celery_config.celery_app worker --loglevel=info
```

For Windows users, you may need to run the following command instead:
```bash
celery -A celery_config.celery_app worker --loglevel=info --pool=solo
```
This will run the worker in a single-threaded mode, which is useful for debugging.

### Example: Enqueue an Addition Task

```bash
curl -X POST "http://localhost:5000/add" -H "Content-Type: application/json" -d '{"x": 5, "y": 10}'
```

### Example: Check Queue Status

```bash
curl "http://localhost:5000/result/c9b7a8c2-f3c7-4e2d-b3e3-e1e0d1c2b3a4"
```

## Project Structure

```
fastapi-queues/
├── main.py                 # FastAPI app and endpoints
├── config.py               # Environment configuration
├── tasks.py                # Celery task definitions
├── celery_config.py        # Celery configuration
├── database/               # Database configuration
│   ├── connection.py       # Database connection
│   └── utils/              # Database utilities
│       └── celery_crud.py  # Celery database utilities
├── requirements.txt
└── README.md
```

## Configuration

- Configure queue backend and worker settings in `.celery.config.py` and via environment variables (`.env` file).

## License

MIT License

---

# FastAPI Queues

A FastAPI-based project for managing background task queues with asynchronous workers. This project demonstrates how to integrate queue processing into a FastAPI application, enabling scalable background job execution.

## Features

- Asynchronous background task processing
- Queue management endpoints
- Integration with popular queue backends (e.g., Redis, in-memory)
- Example producer/consumer patterns

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- [Optional] Redis (for production-grade queues)

## Installation

```bash
git clone https://github.com/davidmuraya/fastapi-queues.git
cd fastapi-queues
pip install -r requirements.txt
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
├── main.py            # FastAPI app and endpoints
├── config.py    # Environment configuration
├── tasks.py   # Celery tasks
├── celery_config.py   # Celery configuration
├── database/   # Database configuration
│   ├── connection.py   # Database connection
│   └── utils/   # Database utilities
│       └── celery_crud.py   # Celery database utilities
├── requirements.txt
└── README.md
```

## Configuration

- Configure queue backend and worker settings in `.celery.config.py` and via environment variables (`.env` file).

## License

MIT License

---
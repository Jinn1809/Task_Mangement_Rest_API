# Task Management REST API

A production-grade REST API for managing Users and Tasks, built with **FastAPI**, **SQLAlchemy**, **SQLite**, and **Pydantic**.

## Tech Stack

- **Python 3.10+**
- **FastAPI** — async web framework
- **SQLAlchemy 2.0** — ORM & database toolkit
- **SQLite** — lightweight relational database
- **Pydantic v2** — data validation & serialization

## Project Structure

```
app/
├── core/
│   └── config.py          # Centralized settings (Pydantic BaseSettings)
├── models/
│   ├── __init__.py
│   ├── base.py            # Base model mixin (id, created_at)
│   ├── user.py            # User ORM model
│   └── task.py            # Task ORM model
├── schemas/
│   ├── __init__.py
│   ├── user.py            # User request/response schemas
│   └── task.py            # Task request/response schemas
├── repositories/
│   ├── __init__.py
│   ├── base.py            # Generic BaseRepository[T]
│   ├── user_repository.py
│   └── task_repository.py
├── services/
│   ├── __init__.py
│   ├── user_service.py
│   └── task_service.py
├── routers/
│   ├── __init__.py
│   ├── users.py
│   └── tasks.py
├── exceptions.py          # Custom exceptions & handlers
├── database.py            # Engine, session, Base
└── main.py                # Application entry point
```

## Quick Start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
uvicorn app.main:app --reload

# 4. Open Swagger UI
# http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint            | Description           |
|--------|---------------------|-----------------------|
| POST   | `/users`            | Create a new user     |
| GET    | `/users`            | List users (paginated)|
| GET    | `/users/{id}/tasks` | Get tasks for a user  |
| POST   | `/tasks`            | Create a new task     |
| GET    | `/tasks`            | List tasks (filterable)|
| GET    | `/tasks/{id}`       | Get task by ID        |
| PATCH  | `/tasks/{id}`       | Update task status    |

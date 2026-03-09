"""
CRUD (Create, Read, Update) operations for User and Task entities.

All data-access logic is centralized here, keeping routers thin
and ensuring a single place to modify database queries (DRY / SRP).
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Task, TaskStatus, User
from app.schemas import TaskCreate, TaskStatusEnum, TaskStatusUpdate, UserCreate


# ===========================================================================
# User CRUD
# ===========================================================================

def create_user(db: Session, data: UserCreate) -> User:
    """Create a new user after validating email uniqueness."""
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A user with email '{data.email}' already exists.",
        )
    user = User(name=data.name, email=data.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session, *, offset: int = 0, limit: int = 100) -> list[User]:
    """Return a paginated list of users."""
    return db.query(User).offset(offset).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> User:
    """Return a single user or raise 404."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{user_id}' not found.",
        )
    return user


# ===========================================================================
# Task CRUD
# ===========================================================================

def create_task(db: Session, data: TaskCreate) -> Task:
    """Create a new task after verifying the referenced user exists."""
    get_user_by_id(db, data.user_id)  # raises 404 if user doesn't exist
    task = Task(
        title=data.title,
        description=data.description,
        user_id=data.user_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(
    db: Session,
    *,
    status_filter: TaskStatusEnum | None = None,
    offset: int = 0,
    limit: int = 100,
) -> list[Task]:
    """List tasks, optionally filtered by status."""
    query = db.query(Task)
    if status_filter:
        model_status = TaskStatus(status_filter.value)
        query = query.filter(Task.status == model_status)
    return query.offset(offset).limit(limit).all()


def get_task_by_id(db: Session, task_id: int) -> Task:
    """Return a single task or raise 404."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id '{task_id}' not found.",
        )
    return task


def update_task_status(db: Session, task_id: int, data: TaskStatusUpdate) -> Task:
    """Update a task's status after verifying it exists."""
    task = get_task_by_id(db, task_id)
    task.status = TaskStatus(data.status.value)
    db.commit()
    db.refresh(task)
    return task


def get_tasks_for_user(db: Session, user_id: int) -> list[Task]:
    """Return all tasks belonging to a specific user (validates user exists)."""
    get_user_by_id(db, user_id)  # raises 404 if user doesn't exist
    return db.query(Task).filter(Task.user_id == user_id).all()

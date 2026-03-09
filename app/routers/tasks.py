"""
Task API endpoints.

Routers are kept thin — they only parse HTTP requests and delegate
to the crud layer (Single Responsibility).
"""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import TaskCreate, TaskResponse, TaskStatusEnum, TaskStatusUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
) -> TaskResponse:
    task = crud.create_task(db, payload)
    return TaskResponse.model_validate(task)


@router.get(
    "",
    response_model=list[TaskResponse],
    summary="List all tasks (optional status filter)",
)
def list_tasks(
    status_filter: TaskStatusEnum | None = Query(default=None, alias="status"),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[TaskResponse]:
    tasks = crud.get_tasks(db, status_filter=status_filter, offset=offset, limit=limit)
    return [TaskResponse.model_validate(t) for t in tasks]


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by its ID",
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> TaskResponse:
    task = crud.get_task_by_id(db, task_id)
    return TaskResponse.model_validate(task)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task's status",
)
def update_task_status(
    task_id: int,
    payload: TaskStatusUpdate,
    db: Session = Depends(get_db),
) -> TaskResponse:
    task = crud.update_task_status(db, task_id, payload)
    return TaskResponse.model_validate(task)

"""
User API endpoints.

Routers are kept thin — they only parse HTTP requests and delegate
to the crud layer (Single Responsibility).
"""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import TaskResponse, UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    user = crud.create_user(db, payload)
    return UserResponse.model_validate(user)


@router.get(
    "",
    response_model=list[UserResponse],
    summary="List all users (paginated)",
)
def list_users(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[UserResponse]:
    users = crud.get_users(db, offset=offset, limit=limit)
    return [UserResponse.model_validate(u) for u in users]


@router.get(
    "/{user_id}/tasks",
    response_model=list[TaskResponse],
    summary="Get all tasks for a specific user",
)
def get_user_tasks(
    user_id: int,
    db: Session = Depends(get_db),
) -> list[TaskResponse]:
    tasks = crud.get_tasks_for_user(db, user_id)
    return [TaskResponse.model_validate(t) for t in tasks]

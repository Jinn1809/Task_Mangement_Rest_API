"""
Pydantic schemas for request/response validation.

All User and Task schemas live in this single file as per the project structure spec.
"""

import enum
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TaskStatusEnum(str, enum.Enum):
    """Allowed status values exposed to API consumers."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


# ---------------------------------------------------------------------------
# User schemas
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    """Schema for creating a new user."""
    name: str = Field(..., min_length=1, max_length=100, examples=["John Doe"])
    email: str = Field(
        ..., min_length=5, max_length=255, examples=["john@example.com"]
    )


class UserResponse(BaseModel):
    """Schema returned when listing or fetching a user."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Task schemas
# ---------------------------------------------------------------------------

class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200, examples=["Fix Login API"])
    description: str = Field(
        default="", max_length=2000, examples=["Resolve authentication bug"]
    )
    user_id: int = Field(..., gt=0, examples=[1])


class TaskStatusUpdate(BaseModel):
    """Schema for updating only the status of a task."""
    status: TaskStatusEnum = Field(..., examples=["completed"])


class TaskResponse(BaseModel):
    """Schema returned when listing or fetching a task."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: TaskStatusEnum
    user_id: int
    created_at: datetime

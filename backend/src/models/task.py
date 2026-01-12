from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, date
from enum import Enum
import json


class PriorityEnum(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    due_date: Optional[str] = Field(default=None)  # Format: YYYY-MM-DD
    due_time: Optional[str] = Field(default=None)  # Format: HH:MM
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)
    tags: Optional[str] = Field(default=None)  # JSON string of tags list
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)

    # Fields for optimistic locking and audit trail
    version: int = Field(default=1)  # For handling concurrent edits
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    # user: "User" = Relationship(back_populates="tasks")  # Commented out to avoid circular import


class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = ""
    due_date: Optional[str] = None  # Format: YYYY-MM-DD
    due_time: Optional[str] = None  # Format: HH:MM
    priority: Optional[PriorityEnum] = PriorityEnum.MEDIUM
    tags: Optional[list[str]] = []  # Will be serialized to JSON string


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None  # Format: YYYY-MM-DD
    due_time: Optional[str] = None  # Format: HH:MM
    priority: Optional[PriorityEnum] = None
    tags: Optional[list[str]] = None  # Will be serialized to JSON string
    completed: Optional[bool] = None


class TaskRead(SQLModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    completed: bool
    due_date: Optional[str]  # Format: YYYY-MM-DD
    due_time: Optional[str]  # Format: HH:MM
    priority: PriorityEnum
    tags: Optional[str]  # JSON string of tags list
    user_id: int
    created_at: datetime
    updated_at: datetime
    version: int
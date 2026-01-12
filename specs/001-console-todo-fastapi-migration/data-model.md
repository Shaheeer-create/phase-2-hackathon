# Data Model: FastAPI Todo Backend

## Overview
This document defines the SQLModel data models for the multi-user FastAPI todo application. The models extend the original console app's data structures with additional fields for multi-user support, authentication, and database persistence.

## Entity Models

### User Model
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Task Model
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from .user import User

class PriorityEnum(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    due_date: Optional[str] = Field(default=None)  # Format: YYYY-MM-DD
    due_time: Optional[str] = Field(default=None)  # Format: HH:MM
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)
    tags: Optional[str] = Field(default=None)  # JSON string of tags list
    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    
    # Fields for optimistic locking and audit trail
    version: int = Field(default=1)  # For handling concurrent edits
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: "User" = Relationship(back_populates="tasks")

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

class TaskRead(Task):
    user_id: int
    version: int
```

### Recurrence Rule Model (Optional Enhancement)
```python
from enum import Enum

class RecurrencePatternEnum(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class RecurrenceRule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pattern: RecurrencePatternEnum
    interval: int = Field(default=1)  # Every N days/weeks/months
    end_date: Optional[str] = Field(default=None)  # Format: YYYY-MM-DD
    max_instances: Optional[int] = Field(default=None)
    task_id: int = Field(foreign_key="task.id", nullable=False)
    
    # Relationship
    task: "Task" = Relationship(back_populates="recurrence_rule")
```

## Database Schema Design

### Indexing Strategy
- `Task.user_id`: Index for efficient user-based queries
- `Task.created_at`: Index for chronological ordering
- `Task.due_date`: Index for due date filtering
- `Task.completed`: Index for completion status filtering
- Composite index on `(user_id, completed)` for common user/completion queries

### Constraints
- `Task.title`: NOT NULL, max length 255
- `Task.user_id`: NOT NULL, foreign key reference to User
- `Task.version`: NOT NULL, default 1 (for optimistic locking)

### Relationships
- `User` to `Task`: One-to-many (one user has many tasks)
- `Task` to `RecurrenceRule`: One-to-one (optional)

## Validation Rules

### Task Validation
- Title: Required, non-empty, max 255 characters
- Description: Optional, max 1000 characters
- Due date: If provided, must be in YYYY-MM-DD format
- Due time: If provided, must be in HH:MM format
- Priority: Must be one of HIGH, MEDIUM, LOW
- Tags: If provided, must be a list of strings
- User ID: Must reference an existing user

### User Validation
- Email: Required, unique, valid email format
- Username: Required, unique, alphanumeric with underscores/hyphens
- Password: Required, minimum 8 characters (validation handled separately)

## State Transitions

### Task Lifecycle
1. **CREATE**: New task inserted with `completed=False`, `version=1`
2. **READ**: Task retrieved with current version
3. **UPDATE**: Task updated with incremented version
4. **TOGGLE COMPLETION**: `completed` field flipped, version incremented
5. **DELETE**: Task marked as deleted or physically removed

### Optimistic Locking
- Each update increments the `version` field
- Updates include WHERE clause checking current version
- If version mismatch occurs, return 409 Conflict error

## Migration Considerations

### From JSON to SQL
- Existing JSON data will be migrated to PostgreSQL
- User ID will need to be assigned during migration
- Tags list will be serialized to JSON string format
- Version field will be initialized to 1 for all existing tasks

### Data Types Mapping
- Python `datetime` → SQL `TIMESTAMP`
- Python `bool` → SQL `BOOLEAN`
- Python `int` → SQL `INTEGER`
- Python `str` → SQL `VARCHAR` or `TEXT`
- Python `list[str]` → SQL `TEXT` (JSON serialized)
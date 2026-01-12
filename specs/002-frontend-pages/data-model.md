# Data Model: Frontend Pages Implementation

## Overview
This document defines the data models for the frontend pages implementation of the Todo application. The models represent the entities used in the authentication and task management system, with a focus on frontend representation and API communication.

## Entity Models

### User Model
```typescript
// frontend/src/types/auth.ts
export interface User {
  id: number;
  email: string;
  username?: string;
  emailVerified?: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface UserRegistration {
  email: string;
  password: string;
  username?: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface UserPublic {
  id: number;
  email: string;
  username?: string;
  emailVerified: boolean;
  createdAt: Date;
}
```

```python
# backend/src/models/user.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    username: Optional[str] = Field(default=None, max_length=100)
    email_verified: bool = Field(default=False)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserRegistration(SQLModel):
    email: str
    password: str
    username: Optional[str] = None


class UserLogin(SQLModel):
    email: str
    password: str


class UserPublic(UserBase):
    id: int
    created_at: datetime
```

### Task Model
```typescript
// frontend/src/types/task.ts
export interface PriorityEnum {
  HIGH = "high";
  MEDIUM = "medium";
  LOW = "low";
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  due_date?: string; // Format: YYYY-MM-DD
  due_time?: string; // Format: HH:MM
  priority: "high" | "medium" | "low";
  tags?: string[]; // Array of tags
  user_id: number;
  created_at: Date;
  updated_at: Date;
  version: number; // For optimistic locking
}

export interface TaskCreate {
  title: string;
  description?: string;
  due_date?: string; // Format: YYYY-MM-DD
  due_time?: string; // Format: HH:MM
  priority?: "high" | "medium" | "low";
  tags?: string[];
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  due_date?: string; // Format: YYYY-MM-DD
  due_time?: string; // Format: HH:MM
  priority?: "high" | "medium" | "low";
  tags?: string[];
  completed?: boolean;
}
```

```python
# backend/src/models/task.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from enum import Enum
import json


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
```

### Session Model
```python
# backend/src/models/session.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token: str = Field(unique=True, nullable=False, max_length=500)
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
```

### Token Model
```python
# backend/src/models/token.py
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
```

## API Request/Response Models

### Authentication Endpoints
```typescript
// Login Request
interface LoginRequest {
  email: string;
  password: string;
}

// Login Response
interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

// Registration Request
interface RegistrationRequest {
  email: string;
  password: string;
  username?: string;
}

// Registration Response
interface RegistrationResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}
```

### Task Endpoints
```typescript
// Get Tasks Response
interface GetTasksResponse {
  tasks: Task[];
  total: number;
}

// Get Task Response
interface GetTaskResponse {
  task: Task;
}

// Create Task Request/Response
interface CreateTaskRequest {
  title: string;
  description?: string;
  due_date?: string;
  due_time?: string;
  priority?: "high" | "medium" | "low";
  tags?: string[];
}

interface CreateTaskResponse {
  task: Task;
}

// Update Task Request/Response
interface UpdateTaskRequest {
  title?: string;
  description?: string;
  due_date?: string;
  due_time?: string;
  priority?: "high" | "medium" | "low";
  tags?: string[];
  completed?: boolean;
}

interface UpdateTaskResponse {
  task: Task;
}

// Error Response
interface ErrorResponse {
  message: string;
  error_code: string;
}
```

## Database Schema Design

### User Table
- `id`: Primary key, auto-incrementing integer
- `email`: Unique, not null, varchar(255)
- `username`: Optional, varchar(100)
- `hashed_password`: Not null, varchar(255), stored using bcrypt
- `email_verified`: Boolean, default false
- `created_at`: Timestamp, default now()
- `updated_at`: Timestamp, default now()

### Task Table
- `id`: Primary key, auto-incrementing integer
- `title`: Not null, varchar(255)
- `description`: Optional, varchar(1000)
- `completed`: Boolean, default false
- `due_date`: Optional, date format (YYYY-MM-DD)
- `due_time`: Optional, time format (HH:MM)
- `priority`: Enum (high, medium, low), default medium
- `tags`: Optional, text field (JSON string of tags array)
- `user_id`: Foreign key referencing user.id
- `version`: Integer, default 1 (for optimistic locking)
- `created_at`: Timestamp, default now()
- `updated_at`: Timestamp, default now()

### Session Table
- `id`: Primary key, auto-incrementing integer
- `user_id`: Foreign key referencing user.id
- `token`: Unique, not null, varchar(500) - JWT token
- `expires_at`: Timestamp for token expiration
- `created_at`: Timestamp, default now()
- `is_active`: Boolean, default true

### Indexing Strategy
- `User.email`: Unique index for fast lookups
- `Task.user_id`: Index for efficient user-based queries
- `Task.completed`: Index for filtering by completion status
- `Task.due_date`: Index for date-based queries
- `Session.token`: Unique index for token validation
- `Session.user_id`: Index for user session queries

### Constraints
- `User.email`: UNIQUE constraint
- `Session.token`: UNIQUE constraint
- `Task.user_id`: FOREIGN KEY constraint to User table
- `Task.title`: NOT NULL constraint
- `User.email`: NOT NULL constraint

## State Transitions

### Task Lifecycle
1. **CREATE**: New task inserted with `completed=false`, `version=1`
2. **READ**: Task retrieved with current version
3. **UPDATE**: Task updated with incremented version
4. **TOGGLE COMPLETION**: `completed` field flipped, version incremented
5. **DELETE**: Task removed from database

### Session Lifecycle
1. **CREATE**: Session initiated on successful login
2. **VALID**: Token is valid and within expiration window
3. **EXPIRED**: Token has passed expiration time
4. **INVALIDATED**: Session deactivated via logout

## Validation Rules

### Task Validation
- Title: Required, non-empty, max 255 characters
- Description: Optional, max 1000 characters
- Due date: If provided, must be in YYYY-MM-DD format
- Due time: If provided, must be in HH:MM format
- Priority: Must be one of HIGH, MEDIUM, LOW
- Tags: If provided, must be an array of strings
- User ID: Must reference an existing user

### User Validation
- Email: Required, unique, valid email format
- Username: Optional, unique if provided, alphanumeric with underscores/hyphens
- Password: Required, minimum 8 characters (validation handled separately)
- Email verification: Optional, defaults to false

### Session Validation
- Token: Required, unique, proper JWT format
- Expiration: Required, must be in the future
- Active status: Boolean, defaults to true
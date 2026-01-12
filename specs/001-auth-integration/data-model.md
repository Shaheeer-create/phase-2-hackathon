# Data Model: Authentication Integration

## Overview
This document defines the data models for the authentication system in the Todo application. The models extend the existing user and task entities with authentication-specific fields and relationships.

## Entity Models

### User Model
```typescript
// frontend/types/auth.ts
export interface User {
  id: number;
  email: string;
  username?: string;
  emailVerified?: Date;
  createdAt: Date;
  updatedAt: Date;
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

### JWT Token Model
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

## Database Schema Design

### User Table
- `id`: Primary key, auto-incrementing integer
- `email`: Unique, not null, varchar(255)
- `username`: Optional, varchar(100)
- `hashed_password`: Not null, varchar(255), stored using bcrypt
- `email_verified`: Boolean, default false
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
- User.email: Unique index for fast lookups
- Session.token: Unique index for token validation
- Session.user_id: Index for user session queries
- Session.expires_at: Index for cleanup operations

### Constraints
- User.email: UNIQUE constraint
- Session.token: UNIQUE constraint
- Session.user_id: FOREIGN KEY constraint to User table
- User.email: NOT NULL constraint

## Validation Rules

### User Validation
- Email: Required, valid email format, unique
- Password: Required, minimum 8 characters (validation handled separately)
- Username: Optional, alphanumeric with underscores/hyphens, unique if provided
- Email verification: Optional, defaults to false

### Session Validation
- Token: Required, unique, proper JWT format
- Expiration: Required, must be in the future
- Active status: Boolean, defaults to true

## State Transitions

### User Lifecycle
1. **REGISTER**: New user created with email, hashed password, email_verified=false
2. **VERIFY_EMAIL**: Email verification process (optional based on spec)
3. **LOGIN**: Session record created with JWT token
4. **LOGOUT**: Session record deactivated
5. **TOKEN_REFRESH**: New session with extended expiration

### Session Lifecycle
1. **CREATE**: Session initiated on successful login
2. **VALID**: Token is valid and within expiration window
3. **EXPIRED**: Token has passed expiration time
4. **INVALIDATED**: Session deactivated via logout or admin action

## Integration Considerations

### With Existing Task Model
- Task records will include user_id foreign key
- Authentication middleware will validate user_id against JWT claims
- Database queries will be filtered by authenticated user

### Migration Requirements
- Existing users (if any) may need to be migrated to new schema
- Passwords will need to be re-hashed with bcrypt if not already
- Session management will be introduced for existing users
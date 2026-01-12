# Architecture: FastAPI Todo Backend

## System Architecture Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI        │    │  Neon PostgreSQL
│   (Next.js)     │◄──►│   Backend        │◄──►│  Database       │
│                 │    │                  │    │                 │
│  - Task Pages   │    │  - Authentication│    │  - User Table   │
│  - Auth Pages   │    │  - Task CRUD    │    │  - Task Table   │
│  - UI Comp.     │    │  - JWT Verif.   │    │  - Indexes      │
└─────────────────┘    │  - Validation   │    └─────────────────┘
                       │  - Error Hand.  │
                       └──────────────────┘
                                │
                       ┌──────────────────┐
                       │  Better Auth     │
                       │  (JWT Service)   │
                       └──────────────────┘
```

## Component Breakdown

### 1. Frontend Layer (Next.js 16+)
- **Pages**: Task management interfaces, authentication flows
- **Components**: Reusable UI elements for tasks, forms, lists
- **Services**: API clients for interacting with backend
- **Authentication**: Better Auth integration for session management

### 2. Backend Layer (FastAPI)
- **Authentication Middleware**: JWT verification and user identification
- **API Routes**: REST endpoints under `/api/{user_id}/...`
- **Business Logic**: Task operations, validation, user isolation
- **Database Services**: SQLModel ORM operations
- **Dependency Injection**: Database sessions, authentication checks

### 3. Authentication Service (Better Auth)
- **Token Generation**: JWT creation with user claims
- **Token Verification**: Signature and expiration validation
- **Shared Secret**: Symmetric key for signing/verification

### 4. Database Layer (Neon Serverless PostgreSQL)
- **User Table**: Stores user accounts and authentication info
- **Task Table**: Stores user tasks with foreign key relationship
- **Indexes**: Optimized for common query patterns
- **Connection Pooling**: Managed by SQLModel/SQLAlchemy

## API Contract Structure

### Authentication Flow
1. User authenticates via Better Auth
2. JWT token issued with user_id claim
3. Token attached to requests as `Authorization: Bearer <token>`
4. Backend verifies token and extracts user_id
5. Request validated against URL user_id for consistency

### Request Lifecycle
1. HTTP Request arrives at FastAPI
2. Authentication dependency validates JWT
3. User ID extracted and compared with URL parameter
4. Database session injected
5. Business logic executed with user isolation
6. Response formatted and returned

## Data Flow

### Task Creation
```
Frontend POST /api/{user_id}/tasks
         ↓
   JWT Verification
         ↓
   User ID Validation (URL vs Token)
         ↓
   SQLModel INSERT with user_id
         ↓
   Created Task Returned
```

### Task Retrieval
```
Frontend GET /api/{user_id}/tasks
         ↓
   JWT Verification
         ↓
   User ID Validation (URL vs Token)
         ↓
   SQLModel SELECT WHERE user_id = ?
         ↓
   Task List Returned
```

## Security Measures

### Authentication
- JWT tokens with HS256 algorithm
- Short-lived access tokens (30 min default)
- Shared secret stored in environment variables

### Authorization
- User ID validation in URL vs JWT
- Database queries filtered by user_id
- No cross-user data access possible

### Input Validation
- Pydantic models for request validation
- SQL injection prevention via ORM
- Rate limiting at infrastructure level

## Technology Stack

### Backend Technologies
- **Framework**: FastAPI for async request handling
- **ORM**: SQLModel for database operations
- **Authentication**: python-jose for JWT handling
- **Password Hashing**: passlib with bcrypt
- **Async Runtime**: uvicorn ASGI server

### Database Technologies
- **Database**: Neon Serverless PostgreSQL
- **Driver**: asyncpg for async database operations
- **Pooling**: SQLAlchemy connection pooling

### Frontend Technologies
- **Framework**: Next.js 16+ with App Router
- **Styling**: Tailwind CSS
- **Auth Integration**: Better Auth client SDK

## Scalability Considerations

### Horizontal Scaling
- Stateless API design allows multiple instances
- Database connection pooling managed efficiently
- JWT tokens eliminate server-side session storage

### Performance Optimization
- Database indexes on user_id and common query fields
- Async request handling for I/O bound operations
- Query optimization through SQLModel

### Future Enhancements
- Redis cache for frequently accessed data
- Background task processing for notifications
- CDN for static assets
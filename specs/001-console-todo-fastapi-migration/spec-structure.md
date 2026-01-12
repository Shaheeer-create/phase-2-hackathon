# Spec Structure: Phase II Todo Application

This document outlines the complete specification structure for the Phase II todo application, covering all aspects from architecture to UI components.

## 1. Overview (`specs/overview.md`)

### Project Purpose
Transform an existing single-user Python console-based Todo application into a multi-user, JWT-secured FastAPI backend service that conforms to defined REST API specifications and integrates with a Next.js frontend.

### Phase II Scope
- Convert console-based task management to web API
- Implement JWT-based authentication and authorization
- Enable multi-user support with data isolation
- Provide full CRUD operations for tasks
- Integrate with Next.js frontend via REST API

### Tech Stack Summary
- Frontend: Next.js 16+ (App Router), Tailwind CSS
- Backend: Python FastAPI, SQLModel ORM
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)

## 2. Architecture (`specs/architecture.md`)

### Frontend–Backend–Auth Interaction
- Frontend communicates with backend via REST API
- Authentication handled by Better Auth
- JWT tokens passed in Authorization header
- User isolation enforced at backend level

### JWT Verification Flow
- User logs in via Better Auth
- JWT issued containing user claims
- Frontend attaches JWT to API requests
- Backend verifies JWT and extracts user identity
- Request validated against user permissions

### Request Lifecycle
1. Client sends authenticated request to API
2. JWT verified by authentication middleware
3. User ID validated against URL parameter
4. Database operation performed with user scoping
5. Response returned to client

## 3. Features

### Task CRUD (`specs/features/task-crud.md`)
- **Task Creation**: POST /api/{user_id}/tasks
- **Task Reading**: GET /api/{user_id}/tasks and GET /api/{user_id}/tasks/{id}
- **Task Updating**: PUT /api/{user_id}/tasks/{id}
- **Task Deletion**: DELETE /api/{user_id}/tasks/{id}
- **Task Completion**: PATCH /api/{user_id}/tasks/{id}/complete

#### User Stories and Acceptance Criteria
- As a user, I want to create tasks via API so that I can add items to my todo list
- As a user, I want to view my tasks via API so that I can see what I need to do
- As a user, I want to update my tasks via API so that I can modify task details
- As a user, I want to delete tasks via API so that I can remove completed items
- As a user, I want to mark tasks as complete via API so that I can track progress

### Authentication (`specs/features/authentication.md`)
- **Login**: Authenticate user and issue JWT
- **Session**: Manage user sessions via JWT
- **JWT Behavior**: Token validation and refresh mechanisms

#### Security Rules
- All API endpoints require valid JWT
- User ID in URL must match JWT claims
- No anonymous access to any endpoint
- Tokens expire after configured time period

## 4. API Specifications (`specs/api/rest-endpoints.md`)

### Endpoint Definitions
- Base URL: `/api/{user_id}/`
- All endpoints require JWT authentication
- Consistent error response format

### Request/Response Contracts
- Request bodies in JSON format
- Response bodies in JSON format
- Standard HTTP status codes
- Consistent error format: `{"message": "...", "error_code": "..."}`

### Error Behavior
- 401: Unauthorized (invalid or missing JWT)
- 403: Forbidden (user ID mismatch or insufficient permissions)
- 404: Not Found (resource does not exist)
- 409: Conflict (concurrent edit detected)
- 422: Unprocessable Entity (validation error)

## 5. Database Schema (`specs/database/schema.md`)

### SQLModel Schema
- User model with authentication fields
- Task model with user relationship
- Proper indexing for performance
- Constraints for data integrity

### Indexing and Constraints
- Index on user_id for efficient queries
- Unique constraints where appropriate
- Foreign key relationships enforced
- Optimistic locking with version field

## 6. UI Specifications

### Pages (`specs/ui/pages.md`)
- **Dashboard**: View all tasks
- **Task Detail**: View individual task
- **Create Task**: Form to create new tasks
- **Edit Task**: Form to update existing tasks
- **Auth Pages**: Login, registration, profile

#### Auth-Protected Routes
- All task-related pages require authentication
- Redirect unauthenticated users to login
- JWT validation on initial page load

### Components (`specs/ui/components.md`)
- **Task List**: Display multiple tasks with filtering
- **Task Card**: Individual task display
- **Task Form**: Create/edit form with validation
- **Navigation**: App navigation elements
- **Auth Components**: Login/logout UI elements
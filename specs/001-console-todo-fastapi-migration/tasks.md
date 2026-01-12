# Implementation Tasks: Console Todo App → FastAPI Web Backend Migration

**Feature**: Console Todo App → FastAPI Web Backend Migration  
**Branch**: `001-console-todo-fastapi-migration`  
**Generated**: 2026-01-08

## Overview

This document outlines the implementation tasks for migrating a single-user Python console-based Todo application to a multi-user, JWT-secured FastAPI backend service. The implementation will leverage SQLModel for database operations with Neon Serverless PostgreSQL, implement proper user isolation, and provide a complete REST API as specified in the OpenAPI contract.

## Implementation Strategy

The implementation follows a phased approach prioritizing foundational components first, followed by user stories in priority order (P1, P2, P3). Each user story phase builds upon the previous work to create a complete, independently testable increment.

**MVP Scope**: User Story 1 (Access Personal Tasks via Web API) provides the core functionality for the minimum viable product.

## Phase 1: Setup

### Goal
Initialize the project structure and configure foundational dependencies.

### Independent Test
The project can be created with all required dependencies installed and basic FastAPI application runs without errors.

### Tasks

- [X] T001 Create backend directory structure per implementation plan
- [X] T002 [P] Create requirements.txt with FastAPI, SQLModel, python-jose, passlib, psycopg
- [X] T003 [P] Initialize main.py with basic FastAPI app
- [X] T004 Create src directory structure per implementation plan
- [X] T005 [P] Create src/core/config.py for application configuration
- [X] T006 [P] Create src/core/database.py for database connection setup
- [X] T007 [P] Create src/core/security.py for JWT and password utilities
- [X] T008 Create tests directory structure per implementation plan

## Phase 2: Foundational Components

### Goal
Implement authentication infrastructure and database models required by all user stories.

### Independent Test
Authentication system generates valid JWTs and database connection is established with proper models.

### Tasks

- [X] T009 [P] Create src/models/__init__.py
- [X] T010 [P] Create src/models/user.py with User model per data-model.md
- [X] T011 [P] Create src/models/task.py with Task model per data-model.md
- [X] T012 [P] Create src/models/enums.py with PriorityEnum per data-model.md
- [X] T013 [P] Create src/api/deps.py with authentication dependencies
- [X] T014 [P] Create src/api/routes/__init__.py
- [X] T015 [P] Create src/services/__init__.py
- [X] T016 [P] Create src/services/auth_service.py for JWT handling
- [X] T017 [P] Create src/services/task_service.py with basic CRUD operations
- [X] T018 [P] Update main.py to include database initialization
- [X] T019 [P] Create src/core/database.py with engine and session setup

## Phase 3: [US1] Access Personal Tasks via Web API

### Goal
Enable registered users to access their personal todo tasks through a web API.

### Priority
P1 (Core functionality that enables the transition from console to web-based access)

### Independent Test
The user can successfully authenticate with a JWT token and retrieve their list of tasks via the API endpoint.

### Acceptance Scenarios
1. Given a user has valid JWT credentials and has created tasks in the system, When the user makes a GET request to `/api/{user_id}/tasks` with a valid JWT, Then the system returns a list of tasks belonging to that user.
2. Given a user has valid JWT credentials, When the user makes a GET request to `/api/{user_id}/tasks/{id}` with a valid JWT, Then the system returns the details of the specific task if it belongs to the user.

### Tasks

- [X] T020 [P] [US1] Create src/api/routes/auth.py with authentication endpoints
- [X] T021 [P] [US1] Create src/api/routes/tasks.py with GET endpoints
- [X] T022 [US1] Implement GET /api/{user_id}/tasks endpoint in task_service
- [X] T023 [US1] Implement GET /api/{user_id}/tasks/{id} endpoint in task_service
- [X] T024 [US1] Add user authentication validation to task endpoints
- [X] T025 [US1] Add user ID validation (URL vs JWT) to task endpoints
- [X] T026 [US1] Add proper error responses per specification (401, 403, 404)
- [X] T027 [US1] Test user can retrieve their own tasks via API
- [X] T028 [US1] Test user cannot access other users' tasks (403 error)

## Phase 4: [US2] Manage Tasks via Web API

### Goal
Enable registered users to create, update, and delete their tasks through a web API.

### Priority
P2 (Extends core functionality to allow full CRUD operations)

### Independent Test
The user can successfully create, update, and delete tasks through the respective API endpoints.

### Acceptance Scenarios
1. Given a user has valid JWT credentials, When the user makes a POST request to `/api/{user_id}/tasks` with valid task data and a valid JWT, Then the system creates a new task associated with the user and returns the created task details.
2. Given a user has valid JWT credentials and an existing task, When the user makes a PUT request to `/api/{user_id}/tasks/{id}` with updated task data and a valid JWT, Then the system updates the task if it belongs to the user.

### Tasks

- [X] T029 [P] [US2] Implement POST /api/{user_id}/tasks endpoint in task_service
- [X] T030 [P] [US2] Implement PUT /api/{user_id}/tasks/{id} endpoint in task_service
- [X] T031 [P] [US2] Implement DELETE /api/{user_id}/tasks/{id} endpoint in task_service
- [X] T032 [US2] Add validation for task creation and updates
- [X] T033 [US2] Add optimistic locking with version field to update operations
- [X] T034 [US2] Add proper error responses for invalid data (422)
- [X] T035 [US2] Test user can create tasks via API
- [X] T036 [US2] Test user can update their own tasks via API
- [X] T037 [US2] Test user can delete their own tasks via API
- [X] T038 [US2] Test concurrent edit detection with optimistic locking (409 error)

## Phase 5: [US3] Secure Task Operations

### Goal
Ensure that user tasks are protected from unauthorized access.

### Priority
P3 (Security is critical for multi-user systems)

### Independent Test
Attempts to access another user's tasks result in appropriate error responses.

### Acceptance Scenarios
1. Given a user has valid JWT credentials for user A, When the user makes a GET request to `/api/{user_B_id}/tasks` with a JWT for user A, Then the system returns a 403 Forbidden error.
2. Given a request without a JWT token, When the user makes any request to `/api/{user_id}/tasks`, Then the system returns a 401 Unauthorized error.

### Tasks

- [X] T039 [P] [US3] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint
- [X] T040 [US3] Add comprehensive user ID validation across all endpoints
- [X] T041 [US3] Implement validation that JWT user ID matches URL user ID
- [X] T042 [US3] Add authentication enforcement to all endpoints
- [X] T043 [US3] Test unauthorized access returns 401 error
- [X] T044 [US3] Test cross-user access returns 403 error
- [X] T045 [US3] Test task completion toggle works correctly
- [X] T046 [US3] Add comprehensive error handling per specification

## Phase 6: Polish & Cross-Cutting Concerns

### Goal
Complete the implementation with proper error handling, documentation, and deployment configuration.

### Independent Test
All functional requirements are met and the backend can run independently via uvicorn.

### Tasks

- [X] T047 Create README.md with setup and usage instructions
- [X] T048 Add comprehensive error response format per specification
- [X] T049 Add database indexing per data-model.md recommendations
- [X] T050 Add request/response validation with Pydantic models
- [X] T051 Add logging for security events and errors
- [X] T052 Add environment variable configuration for database URL and JWT secret
- [X] T053 Test all API endpoints with proper authentication
- [X] T054 Run complete test suite to verify all requirements
- [X] T055 Verify all functional requirements (FR-001 through FR-012) are met
- [X] T056 Verify all success criteria (SC-001 through SC-006) are achieved
- [X] T057 Test backend runs independently via uvicorn

## Dependencies

### User Story Completion Order
1. US1 (Access Personal Tasks) - Foundation for all other stories
2. US2 (Manage Tasks) - Builds on authentication and user isolation from US1
3. US3 (Secure Operations) - Depends on all previous functionality

### Critical Path Dependencies
- T001-T019 (Setup and Foundation) must complete before any user story tasks
- US1 must complete before US2 and US3
- Authentication infrastructure (T009-T018) required by all user stories

## Parallel Execution Opportunities

### Per User Story
- **US1**: T020-T021 (route creation) can run in parallel with T022-T023 (service implementation)
- **US2**: T029-T031 (endpoint implementation) can run in parallel
- **US3**: T039 (PATCH endpoint) can be developed in parallel with security enhancements

### Across Stories
- Model creation (T010-T012) can happen once in Phase 2 and be used by all stories
- Authentication infrastructure (T013, T016) supports all stories
- Database setup (T019) supports all stories

## Implementation Notes

1. **Optimistic Locking**: Implemented using the `version` field as specified in the requirements
2. **User Isolation**: Enforced by validating JWT user ID matches URL user ID parameter
3. **Error Format**: Consistent JSON format `{"message": "...", "error_code": "..."}` as specified
4. **HTTP Status Codes**: Proper codes (401, 403, 404, 409, 422) as specified in requirements
5. **Task Properties**: Full set of properties as defined in the specification
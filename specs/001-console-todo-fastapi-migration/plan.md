# Implementation Plan: Console Todo App → FastAPI Web Backend Migration

**Branch**: `001-console-todo-fastapi-migration` | **Date**: 2026-01-08 | **Spec**: [link to spec.md]
**Input**: Feature specification from `/specs/001-console-todo-fastapi-migration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Migration of a single-user Python console-based Todo application to a multi-user, JWT-secured FastAPI backend service. The implementation will leverage SQLModel for database operations with Neon Serverless PostgreSQL, implement proper user isolation, and provide a complete REST API as specified in the OpenAPI contract. The approach involves refactoring existing business logic from the console app while adding multi-user support, authentication, and web API capabilities.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: FastAPI, SQLModel, python-jose, passlib, psycopg
**Storage**: Neon Serverless PostgreSQL via SQLModel ORM
**Testing**: pytest, openapi-spec-validator
**Target Platform**: Linux server (cloud deployment ready)
**Project Type**: Web application (backend API service)
**Constraints**: JWT-authenticated endpoints, user data isolation, optimistic locking for concurrent edits
**Scale/Scope**: Multi-user support with proper data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Spec-First Development: All implementation will be derived from written specifications
- [x] Single Source of Truth: Code will conform to specs, not vice versa
- [x] Security by Default: Authentication, authorization, and user isolation will be implemented
- [x] Agentic Discipline: qwen Code agents will operate within defined roles and skills
- [x] Minimal but Complete: Specs will be well-scoped rather than fragmented

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo-fastapi-migration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── openapi.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── task_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       └── tasks.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── requirements.txt
└── README.md
```

**Structure Decision**: Web application with dedicated backend service following FastAPI best practices. The structure separates concerns into models, services, API routes, and core utilities. This follows the recommended approach for larger FastAPI applications and allows for clear separation between business logic and API presentation.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (none) | (none) | (none) |

## Phased Implementation

### Phase 1: Research
- Analyze existing console app logic in phase-1
- Identify reusable task operations and business logic
- Extract entity definitions from feature specification
- Document current data models and operations

**Objectives**:
- Understand existing console application architecture
- Map console operations to web API endpoints
- Identify components that can be refactored vs. rewritten

**Validation Checkpoints**:
- [ ] All console app functionality catalogued
- [ ] Mapping between console operations and API endpoints defined
- [ ] Reusable components identified

### Phase 2: Foundation
- Write core specifications based on feature spec
- Define SQLModel database schema
- Configure FastAPI application structure
- Implement JWT authentication foundation

**Objectives**:
- Set up FastAPI project with required dependencies
- Implement SQLModel models matching spec requirements
- Configure database connection to Neon PostgreSQL
- Implement JWT authentication middleware

**Validation Checkpoints**:
- [ ] FastAPI application skeleton created
- [ ] SQLModel models match specification requirements
- [ ] Database connection established
- [ ] JWT authentication foundation implemented
- [ ] User isolation mechanism designed

### Phase 3: Implementation
- Implement specified API endpoints:
  - GET `/api/{user_id}/tasks`
  - GET `/api/{user_id}/tasks/{id}`
  - POST `/api/{user_id}/tasks`
  - PUT `/api/{user_id}/tasks/{id}`
  - PATCH `/api/{user_id}/tasks/{id}/complete`
  - DELETE `/api/{user_id}/tasks/{id}`
- Implement business logic for task operations
- Enforce user data isolation for all operations
- Implement error handling with specified response format

**Objectives**:
- Implement all required REST endpoints
- Apply JWT authentication to all endpoints
- Enforce user isolation on all operations
- Implement optimistic locking for concurrent edits
- Ensure proper error responses per specification

**Validation Checkpoints**:
- [ ] All specified endpoints implemented (GET, POST, PUT, DELETE, PATCH)
- [ ] JWT authentication enforced on all endpoints
- [ ] User data isolation implemented (users can only access own tasks)
- [ ] Error responses follow specified JSON format
- [ ] HTTP status codes match specification (401, 403, 404, 422)
- [ ] Optimistic locking implemented with version field
- [ ] Task entity properties match specification

### Phase 4: Validation
- Validate API behavior against OpenAPI specification
- Test all user stories and acceptance scenarios
- Verify security requirements (authentication, authorization)
- Confirm all functional requirements are met

**Objectives**:
- Execute tests for all user stories
- Validate API compliance with specification
- Verify security measures are effective
- Confirm all functional requirements satisfied

**Validation Checkpoints**:
- [ ] User Story 1 satisfied (access personal tasks via API)
- [ ] User Story 2 satisfied (manage tasks via API)
- [ ] User Story 3 satisfied (secure task operations)
- [ ] All acceptance scenarios pass
- [ ] API endpoints match OpenAPI specification
- [ ] All functional requirements (FR-001 through FR-012) met
- [ ] Success criteria (SC-001 through SC-006) achieved
- [ ] Backend runs independently via `uvicorn`

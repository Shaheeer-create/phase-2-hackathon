# Research: Console Todo App → FastAPI Web Backend Migration

## Overview
This document captures research findings for migrating the console-based Todo application to a JWT-secured FastAPI web backend service. The research addresses all "NEEDS CLARIFICATION" items from the feature specification.

## Resolved Clarifications

### 1. Task Entity Properties
**Original Question**: What are the specific properties for the Task entity?
**Answer**: Based on analysis of `phase-1/src/models/task.py`, the Task entity has the following properties:
- `id` (int): Unique sequential identifier
- `title` (str): Task title/name (required, must not be empty)
- `description` (str): Task description (optional, default empty)
- `completed` (bool): Task completion status (False=pending, True=completed)
- `due_date` (Optional[str]): Due date in YYYY-MM-DD format (optional)
- `due_time` (Optional[str]): Due time in HH:MM format (optional)
- `priority` (Optional[Priority]): Task priority (High/Medium/Low, default Medium)
- `tags` (List[str]): List of categorization tags (default empty list)
- `recurrence_rule` (Optional[RecurrenceRule]): Recurrence schedule for recurring tasks (optional)
- `reminder` (Optional[Reminder]): Scheduled notification for this task (optional)
- `user_id` (int): Foreign key linking to User (to be added for multi-user support)

For the FastAPI migration, we'll need to add a `user_id` field to enable user data isolation.

### 2. JWT Token Transmission
**Original Question**: How should JWT tokens be transmitted with requests?
**Answer**: As specified in the requirements, JWT tokens should be transmitted using the Authorization header with Bearer scheme: `Authorization: Bearer <token>`

### 3. Error Response Format
**Original Question**: What format should error responses follow?
**Answer**: Error responses should follow a consistent JSON format: `{"message": "error description", "error_code": "ERROR_CODE"}`

### 4. Non-existent Task Updates
**Original Question**: What happens when updating a non-existent task?
**Answer**: Based on analysis of `phase-1/src/services/task_manager.py`, attempting to update a non-existent task raises a `TaskNotFoundError`. In the FastAPI migration, this should return a 404 Not Found HTTP status code.

### 5. Concurrent Edits Handling
**Original Question**: How should concurrent edits be handled?
**Answer**: The current implementation doesn't handle concurrent edits. For the FastAPI migration, we'll implement optimistic locking using a `version` integer field as specified in the requirements.

## Technology Stack Analysis

### Current Implementation (Phase 1)
- Language: Python 3.10+
- Framework: Pure Python with dataclasses
- Storage: JSON file-based (via `JSONStorage` class)
- Architecture: Single-user, console-based application
- Dependencies: Standard library only

### Target Implementation (Phase 2)
- Language: Python 3.10+
- Framework: FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)
- Architecture: Multi-user, web API backend

## Key Components to Migrate

### 1. Task Model
The current `Task` dataclass needs to be converted to a SQLModel model with:
- Database fields matching the original properties
- Additional `user_id` field for multi-user support
- `version` field for optimistic locking
- Proper indexing for performance

### 2. Task Manager Service
The `TaskManager` class contains all business logic for:
- Creating, reading, updating, and deleting tasks
- Searching and filtering tasks
- Managing recurring tasks
- Handling reminders
- Validating inputs

This logic needs to be adapted to work with:
- SQLModel database operations
- JWT-based user authentication
- User data isolation

### 3. Storage Layer
The current JSON-based storage needs to be replaced with:
- SQLModel models
- Neon Serverless PostgreSQL database
- Proper connection pooling and async operations

### 4. Authentication & Authorization
New components needed:
- JWT token verification middleware
- User identification and validation
- Cross-user access prevention

## Migration Strategy

### Approach: Refactor and Reuse Logic
Based on the analysis, the most efficient approach is to refactor and reuse the existing business logic rather than rewriting everything from scratch. This approach:
- Preserves tested business logic
- Reduces development time
- Maintains feature parity
- Minimizes the risk of introducing bugs

### Specific Steps:
1. Adapt the `Task` model to SQLModel with additional fields
2. Refactor `TaskManager` methods to work with database operations
3. Implement JWT authentication layer
4. Add user isolation mechanisms
5. Maintain all existing functionality (search, filter, sort, etc.)

## Potential Challenges

### 1. Concurrency Control
The current implementation assumes single-user access. The multi-user system will need:
- Proper transaction handling
- Optimistic locking implementation
- Conflict resolution for concurrent edits

### 2. Data Migration
Existing JSON data needs to be migrated to PostgreSQL, potentially with:
- A migration script
- User assignment for existing tasks
- Preservation of all task properties

### 3. Performance Considerations
- JSON file operations vs. database queries
- Indexing strategy for common operations
- Connection pooling for database access

## Best Practices for FastAPI + SQLModel

### 1. Async Operations
- Use async/await for database operations
- Implement proper connection pooling
- Handle concurrent requests efficiently

### 2. Pydantic Models
- Create separate models for API requests/responses
- Use different models for create, update, and read operations
- Implement proper validation

### 3. Dependency Injection
- Use FastAPI dependencies for authentication
- Inject database sessions properly
- Implement reusable components

## Conclusion
The research has successfully resolved all "NEEDS CLARIFICATION" items from the feature specification. The existing console application provides a solid foundation for the FastAPI migration, with well-defined business logic that can be adapted for the web backend. The refactoring approach will preserve valuable functionality while adding the required multi-user and web API capabilities.
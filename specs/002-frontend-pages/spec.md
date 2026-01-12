# Feature Specification: Frontend Pages for Todo Application

**Feature Branch**: `002-frontend-pages`
**Created**: 2026-01-08
**Status**: Draft
**Input**: User description: "Phase II: Frontend Pages for Full-Stack Todo App Target audience: Frontend developers and qwen Code agents implementing Next.js pages in the Todo App Focus: Implement responsive, authenticated pages for task management and user login/signup flows using Next.js App Router, integrating JWT-secured backend endpoints Success criteria: - Pages implemented according to UI spec and Tailwind CSS guidelines - Pages are fully functional with JWT authentication - Users can navigate login, signup, task dashboard, and task detail pages - API client used for all backend requests, JWT token attached automatically - Pages use reusable components (TaskCard, TaskList, TaskForm, Navbar) - Error handling and redirects implemented correctly - Fully compatible with existing /api/tasks backend Constraints: - Next.js 16+ with App Router - TypeScript and Tailwind CSS only - No manual coding outside qwen Code - Pages must integrate with backend auth system and JWT flow - Must be modular and reusable (server/client component separation) Not building: - Advanced styling or animations beyond Tailwind defaults - Social login flows - Admin dashboards or multi-user management - AI chatbot integration (Phase III) --- # Feature: Frontend Pages ## Pages to Implement 1. **/login** - Login form (email + password) - Error messages for invalid credentials - On success: store JWT, redirect to /tasks 2. **/signup** - Signup form (email + password) - Error messages for invalid email/password - On success: store JWT, redirect to /tasks 3. **/tasks** - Dashboard showing all user tasks - Filter by status (all, pending, completed) - Buttons for create/update/delete tasks 4. **/tasks/[id]** - Task detail view - Update task status or details - Delete task option 5. **Navbar** - Shows login/logout state - Links to /tasks, /login, /signup - Logout clears JWT token 6. **Error / 404 page** - Display user-friendly error messages - Redirects if user is unauthorized --- # Subagents and Skills to Use ## Spec Architect Agent - **Skills:** spec-writer, spec-validator - **Use:** Ensure page specifications are complete, consistent, and match existing Spec-Kit guidelines ## Frontend Engineer Agent - **Skills:** nextjs-ui-builder, api-client - **Use:** Generate Next.js pages and components, integrate API client, attach JWT to requests ## Auth & Integration Agent - **Skills:** better-auth-config, auth-integration - **Use:** Implement login/signup flows, handle JWT storage and redirects ## MCP / Context Knowledge - **Use:** Reference @specs/features/authentication.md, @specs/api/frontend-api.md, @specs/ui/components.md - **Purpose:** Ensure pages are consistent with authentication, API client, and component specs; reuse existing knowledge --- # Implementation Notes - **Frontend Routing** - Pages use Next.js App Router structure (/app/login, /app/signup, /app/tasks, /app/tasks/[id]) - **Component Usage** - TaskCard → render individual tasks - TaskList → render list of tasks - TaskForm → create/update tasks - Navbar → user navigation + login/logout - **JWT Handling** - Store JWT in secure client-side session or context - Attach JWT to API calls automatically via api-client - Redirect unauthorized users to /login - **Error Handling** - Show inline form errors - Handle 401/403 API responses with page redirects - Display 404 for missing tasks or invalid routes"

**Constitution Compliance**: This spec adheres to the project constitution by following spec-driven development principles.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Authentication and Login (Priority: P1)

As a returning user, I want to log in to the application so that I can access my tasks and maintain my session.

**Why this priority**: This is the most critical functionality for existing users to access their data. Without login capability, users cannot use the application.

**Independent Test**: A returning user can successfully log in with their credentials, receive a JWT token, and be redirected to the tasks page.

**Acceptance Scenarios**:

1. **Given** a user is on the login page, **When** the user enters their email and password and submits the form, **Then** the system validates credentials and returns a JWT token, storing it securely and redirecting to the tasks page.
2. **Given** a user enters invalid credentials, **When** the user submits the login form, **Then** the system displays an appropriate error message without revealing whether the email or password was incorrect.

---

### User Story 2 - New User Registration (Priority: P2)

As a new user, I want to register for an account so that I can start using the todo application.

**Why this priority**: This enables new user acquisition and is essential for growing the user base. Without registration, the application cannot attract new users.

**Independent Test**: A new user can successfully register with email and password, receive a JWT token, and be redirected to the tasks page.

**Acceptance Scenarios**:

1. **Given** a user is on the signup page, **When** the user enters a valid email and password and submits the form, **Then** the system creates a new account, returns a JWT token, stores it securely, and redirects to the tasks page.
2. **Given** a user enters invalid registration data (invalid email format, weak password), **When** the user submits the signup form, **Then** the system displays appropriate validation error messages.

---

### User Story 3 - Task Dashboard Access (Priority: P3)

As a logged-in user, I want to view my tasks on a dashboard so that I can manage my todo items effectively.

**Why this priority**: This is the core functionality that users expect after authentication. It provides the main value proposition of the application.

**Independent Test**: An authenticated user can access the tasks dashboard and see their list of tasks with filtering capabilities.

**Acceptance Scenarios**:

1. **Given** a user is logged in with a valid JWT token, **When** the user navigates to the tasks page, **Then** the system displays the user's tasks with options to filter by status (all, pending, completed).
2. **Given** a user is not logged in, **When** the user attempts to access the tasks page, **Then** the system redirects to the login page.

---

### User Story 4 - Task Management (Priority: P4)

As a user, I want to create, update, and delete my tasks so that I can manage my todo list effectively.

**Why this priority**: This provides the core task management functionality that makes the application useful for users.

**Independent Test**: A logged-in user can create, update, and delete tasks through the appropriate UI controls.

**Acceptance Scenarios**:

1. **Given** a user is on the tasks page, **When** the user creates a new task with valid data, **Then** the system saves the task and displays it in the task list.
2. **Given** a user is viewing a specific task, **When** the user updates the task details, **Then** the system saves the changes and reflects them in the UI.
3. **Given** a user wants to remove a task, **When** the user deletes the task, **Then** the system removes it from the task list.

---

### Edge Cases

- What happens when a JWT token expires while the user is on a page?
- How does the system handle network errors during API requests?
- What occurs when a user tries to access a task that doesn't exist or doesn't belong to them?
- How does the system behave when the backend API is temporarily unavailable?
- What happens when a user tries to register with an email that already exists?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a login page at `/login` with email and password fields
- **FR-002**: System MUST authenticate users and store JWT tokens securely in HttpOnly cookies
- **FR-003**: System MUST redirect authenticated users from login/signup pages to `/tasks`
- **FR-004**: System MUST provide a signup page at `/signup` with email and password fields
- **FR-005**: System MUST validate email format and password strength on both login and signup forms
- **FR-006**: System MUST redirect users to `/tasks` after successful authentication (login or signup)
- **FR-007**: System MUST display user-friendly error messages for authentication failures in standard format: `{"message": "error description", "error_code": "ERROR_CODE"}`
- **FR-008**: System MUST provide a tasks dashboard at `/tasks` showing all user tasks with backend filtering by status (all, pending, completed) using query parameters
- **FR-009**: System MUST allow filtering tasks by status (all, pending, completed) on the tasks page using backend filtering via query parameters
- **FR-010**: System MUST provide a task detail page at `/tasks/[id]` for viewing and editing specific tasks with all properties (title, description, completed, due_date, due_time, priority, tags, user_id, created_at, updated_at, version)
- **FR-011**: System MUST implement a navigation bar showing login/logout state and appropriate links
- **FR-012**: System MUST clear JWT token and redirect to login page when user logs out
- **FR-013**: System MUST attach JWT token to all authenticated API requests automatically via centralized API client with interceptors
- **FR-014**: System MUST redirect unauthenticated users attempting to access protected routes to `/login`
- **FR-015**: System MUST display a user-friendly 404 page for invalid routes
- **FR-016**: System MUST handle API errors gracefully with appropriate user feedback in standard format
- **FR-017**: System MUST implement responsive design that works on mobile and desktop devices
- **FR-018**: System MUST provide visual feedback during loading states (API requests, page transitions)
- **FR-019**: System MUST prevent cross-site request forgery (CSRF) attacks where applicable
- **FR-020**: System MUST ensure all pages are accessible according to WCAG 2.1 AA standards

### Key Entities

- **User Session**: Represents the authenticated state of a user with associated JWT token stored in HttpOnly cookies
- **Task**: Represents a user's todo item with properties: id, title, description, completed, due_date, due_time, priority (high/medium/low), tags (JSON string), user_id, created_at, updated_at, version (for optimistic locking)
- **Navigation State**: Represents the current page and user authentication status for proper navigation

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully log in with valid credentials and be redirected to the tasks page within 3 seconds (95% of attempts)
- **SC-002**: Users can successfully register with valid email/password and be redirected to the tasks page within 5 seconds (95% of attempts)
- **SC-003**: 95% of authenticated users can view their tasks on the dashboard within 2 seconds of page load
- **SC-004**: 99% of unauthorized access attempts to protected routes result in redirect to login page
- **SC-005**: All pages load successfully on both desktop (1920x1080) and mobile (375x667) screen sizes
- **SC-006**: All form submissions provide immediate validation feedback (under 500ms)
- **SC-007**: API requests properly attach JWT tokens with 99.9% success rate for authenticated requests
- **SC-008**: Error pages provide helpful information and navigation options with 100% success rate

## Clarifications

### Session 2026-01-08

- Q: What properties should be included in the Task entity? → A: Include all properties (title, description, completed, due_date, due_time, priority, tags, user_id, created_at, updated_at, version)
- Q: How should JWT tokens be stored for security? → A: HttpOnly cookies (secure against XSS, automatically sent with requests)
- Q: What format should error responses follow? → A: Standard format: `{"message": "error description", "error_code": "ERROR_CODE"}`
- Q: Where should task filtering occur? → A: Backend filtering using query parameters (more efficient, secure)
- Q: How should the API client be implemented? → A: Centralized API client (e.g., using Axios/Fetch with interceptors)
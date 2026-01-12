<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles: 
- Spec-First Development
- Single Source of Truth  
- Security by Default
- Agentic Discipline
- Minimal but Complete
Added sections: Key Standards, Constraints, Success Criteria, Non-Goals, Authority
Removed sections: None
Templates requiring updates: 
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated  
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ✅ updated
Follow-up TODOs: None
-->

# Spec-Driven Full-Stack Todo Web Application Constitution

## Core Principles

### Spec-First Development
All implementation must be derived from written specifications. No feature is implemented without an approved spec.

### Single Source of Truth
Specs define behavior. Code must conform to specs, not vice versa.

### Security by Default
Authentication, authorization, and user isolation are mandatory. No endpoint may expose cross-user data.

### Agentic Discipline
qwen Code agents operate within defined roles and skills. Agents do not exceed their responsibility boundaries.

### Minimal but Complete
Prefer fewer, well-scoped specs over many fragmented documents.

## Key Standards

### Specification Standards
- All specs must follow Spec-Kit Plus conventions
- Specs must be organized by type:
  - features/
  - api/
  - database/
  - ui/
- Acceptance criteria are required for every feature

### Implementation Standards
- No manual coding outside qwen Code execution
- Backend strictly follows FastAPI + SQLModel
- Frontend strictly follows Next.js App Router patterns

### Authentication & Security
- JWT-based authentication is mandatory
- Shared secret via environment variables only
- Backend never trusts client-provided user identifiers
- All data access is filtered by authenticated user

### API Standards
- RESTful conventions
- JSON-only responses
- Proper HTTP status codes (401, 403, 404, 422)
- Authorization required for all endpoints

## Constraints

### Technology Constraints
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Auth: Better Auth (JWT-based)
- Dev Workflow: Spec-Kit Plus + qwen Code

### Workflow Constraints
- Write spec → review → implement
- No direct code edits without spec reference
- Phase-based development only

### Scope Constraints (Phase II)
- Task CRUD operations
- User authentication
- JWT-secured API
- Responsive frontend UI
- Persistent storage

## Success Criteria

- All implemented features trace directly to specs
- Every API request requires valid JWT
- Users can only access their own tasks
- Backend and frontend operate independently but securely
- qwen Code can navigate and modify the repo using specs alone
- Project is reviewable, reproducible, and hackathon-ready

## Non-Goals (Explicitly Out of Scope)

- Advanced AI agents or autonomous planning
- Real-time collaboration features
- Complex role-based permissions
- Mobile-native applications (web-only)

## Authority

- The sp.constitution overrides all other documents
- If conflict exists:
  sp.constitution → specs → qwen.md → code

**Version**: 1.1.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-08
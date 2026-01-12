---
id: 1
title: Update Project Constitution
stage: constitution
date_iso: 2026-01-08
surface: agent
model: qwen
feature: none
branch: main
user: user
command: /sp.constitution
labels:
  - constitution
  - governance
  - spec-driven
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests_yaml: []
---

# Update Project Constitution

## User Input

```
/sp.constitution 

Project: Spec-Driven Full-Stack Todo Web Application (Hackathon II)

Purpose:
Build a secure, multi-user, full-stack Todo web application using a strict
spec-driven and agentic development workflow. The project evolves from a
console app into a production-ready web system with authentication,
persistent storage, and a clean frontend-backend separation.

---

Core Principles:

- **Spec-First Development**
  All implementation must be derived from written specifications.
  No feature is implemented without an approved spec.

- **Single Source of Truth**
  Specs define behavior. Code must conform to specs, not vice versa.

- **Security by Default**
  Authentication, authorization, and user isolation are mandatory.
  No endpoint may expose cross-user data.

- **Agentic Discipline**
  qwen Code agents operate within defined roles and skills.
  Agents do not exceed their responsibility boundaries.

- **Minimal but Complete**
  Prefer fewer, well-scoped specs over many fragmented documents.

---

Key Standards:

- **Specification Standards**
  - All specs must follow Spec-Kit Plus conventions
  - Specs must be organized by type:
    - features/
    - api/
    - database/
    - ui/
  - Acceptance criteria are required for every feature

- **Implementation Standards**
  - No manual coding outside qwen Code execution
  - Backend strictly follows FastAPI + SQLModel
  - Frontend strictly follows Next.js App Router patterns

- **Authentication & Security**
  - JWT-based authentication is mandatory
  - Shared secret via environment variables only
  - Backend never trusts client-provided user identifiers
  - All data access is filtered by authenticated user

- **API Standards**
  - RESTful conventions
  - JSON-only responses
  - Proper HTTP status codes (401, 403, 404, 422)
  - Authorization required for all endpoints

---

Constraints:

- **Technology Constraints**
  - Frontend: Next.js 16+ (App Router)
  - Backend: Python FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Auth: Better Auth (JWT-based)
  - Dev Workflow: Spec-Kit Plus + qwen Code

- **Workflow Constraints**
  - Write spec → review → implement
  - No direct code edits without spec reference
  - Phase-based development only

- **Scope Constraints (Phase II)**
  - Task CRUD operations
  - User authentication
  - JWT-secured API
  - Responsive frontend UI
  - Persistent storage

---

Success Criteria:

- All implemented features trace directly to specs
- Every API request requires valid JWT
- Users can only access their own tasks
- Backend and frontend operate independently but securely
- qwen Code can navigate and modify the repo using specs alone
- Project is reviewable, reproducible, and hackathon-ready

---

Non-Goals (Explicitly Out of Scope):

- Advanced AI agents or autonomous planning
- Real-time collaboration features
- Complex role-based permissions
- Mobile-native applications (web-only)

---

Authority:

- The sp.constitution overrides all other documents
- If conflict exists:
  sp.constitution → specs → qwen.md → code
```

## Response Summary

Updated the project constitution file at `.specify/memory/constitution.md` with the specified principles and standards for the Spec-Driven Full-Stack Todo Web Application. The constitution now includes:

- Core Principles: Spec-First Development, Single Source of Truth, Security by Default, Agentic Discipline, and Minimal but Complete
- Key Standards for specifications, implementation, authentication & security, and API standards
- Technology and workflow constraints
- Success criteria and non-goals
- Authority hierarchy

Also updated the template files to align with the new constitution:
- `.specify/templates/plan-template.md` - Added constitution check items
- `.specify/templates/spec-template.md` - Added constitution compliance note
- `.specify/templates/tasks-template.md` - Added constitution compliance note

The constitution version was updated from 1.0.0 to 1.1.0 to reflect the significant additions and changes.

## Outcome

The project constitution has been successfully updated with all specified principles and standards. Template files have been modified to ensure consistency with the new constitution. The constitution now serves as the authoritative document for the project's development workflow and standards.

## Evaluation

The implementation successfully created a comprehensive constitution that captures all the specified principles and requirements. The template files have been updated to maintain consistency with the new constitution. The version has been properly incremented according to semantic versioning rules (from 1.0.0 to 1.1.0) since new principles and sections were added.
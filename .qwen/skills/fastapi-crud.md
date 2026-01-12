---
name: "fastapi-crud"
description: "Implement RESTful CRUD APIs using FastAPI and SQLModel strictly from specifications. Use when building backend endpoints."
version: "1.0.0"
---

# FastAPI CRUD Skill

## When to Use This Skill

- Spec defines REST endpoints
- Backend implementation requested
- SQLModel is required

## Procedure

1. **Read API + database specs**
2. **Define SQLModel models**
3. **Implement route handlers**
4. **Enforce user ownership**
5. **Return JSON responses**

## Output Format

- FastAPI routes under `/api`
- Pydantic request/response models

## Quality Criteria

- All queries filtered by authenticated user
- Proper HTTP status codes
- No business logic in routes

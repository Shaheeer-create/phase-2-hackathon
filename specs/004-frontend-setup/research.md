# Research: Frontend Setup and UI Components for Tasks Web App

## Overview
This document captures research findings for implementing the authentication system for the Todo application. The research addresses all technical decisions needed for the frontend setup with Next.js, Better Auth, and JWT-based authentication.

## Technology Research

### Next.js 16+ App Router Implementation
- **Decision**: Use Next.js 16+ with App Router for the frontend
- **Rationale**:
  - Modern file-based routing system with better performance
  - Built-in support for server and client components
  - Enhanced data fetching capabilities
  - Better SEO and streaming capabilities
- **Alternatives considered**:
  - Pages Router: Legacy approach, App Router is now recommended
  - Other frameworks: Sticking with Next.js as specified in constraints

### Better Auth Integration
- **Decision**: Use Better Auth for frontend authentication
- **Rationale**:
  - Seamless Next.js integration with App Router support
  - Built-in JWT handling capabilities
  - Good documentation and community support
  - Supports email/password authentication out of the box
- **Alternatives considered**:
  - NextAuth.js: Also good but Better Auth has more modern approach
  - Clerk: More complex and costly for basic auth needs
  - Custom solution: Would require more development time and security considerations

### JWT Token Handling in Next.js
- **Decision**: Store JWT tokens in HttpOnly cookies for security
- **Rationale**:
  - Protection against XSS attacks
  - Automatic inclusion in requests to same origin
  - Better security than localStorage
- **Alternatives considered**:
  - localStorage: Vulnerable to XSS attacks
  - sessionStorage: Lost on tab close but still vulnerable to XSS
  - Memory storage: Tokens lost on page refresh

### FastAPI and SQLModel Integration
- **Decision**: Use FastAPI with SQLModel for the backend
- **Rationale**:
  - FastAPI provides excellent performance and automatic API documentation
  - SQLModel offers compatibility with SQLAlchemy while supporting Pydantic
  - Strong type validation and autocompletion
  - Async support for handling concurrent requests efficiently
- **Alternatives considered**:
  - Flask: Less performant and lacks automatic documentation
  - Django: Heavier framework than needed for this API
  - Other ORMs: SQLModel chosen for compatibility with project constraints

### PostgreSQL Database Design
- **Decision**: Use Neon Serverless PostgreSQL with proper indexing
- **Rationale**:
  - Serverless option provides automatic scaling
  - SQLModel compatibility for ORM operations
  - ACID compliance for data integrity
  - Support for JSON fields for flexible data storage
- **Alternatives considered**:
  - SQLite: Less suitable for multi-user production applications
  - MongoDB: Doesn't fit well with SQLModel ORM approach

## Architecture Research

### Frontend-Backend Authentication Flow
- **Decision**: Frontend handles authentication via Better Auth, backend verifies JWT
- **Rationale**:
  - Separates concerns between frontend and backend
  - Backend remains stateless
  - Standard approach for modern web applications
- **Flow**:
  1. User authenticates via Better Auth on frontend
  2. JWT token is issued and stored in HttpOnly cookie
  3. Frontend includes JWT in Authorization header for API requests
  4. Backend verifies JWT and extracts user information
  5. Backend enforces user-level access control

### User Isolation Strategy
- **Decision**: Enforce user isolation at the database and application layer
- **Rationale**:
  - Critical for security and privacy
  - Required by specification
  - Multiple layers of protection
- **Implementation**:
  - Database queries filtered by user_id
  - Application logic verifies user_id matches JWT claims
  - URL parameter validation against JWT claims

## Security Considerations

### JWT Security Best Practices
- Use strong secret for signing (SECRET_KEY)
- Set appropriate expiration times (7 days as specified)
- Validate token on every authenticated request
- Include user identity in token claims
- Never store sensitive data in JWT payload

### Session Management
- Secure cookie attributes (HttpOnly, Secure, SameSite)
- Proper logout mechanism that clears tokens
- Token refresh strategies if needed in future
- Prevention of session fixation attacks

### Rate Limiting Implementation
- **Decision**: Implement rate limiting per IP address on authentication endpoints
- **Rationale**:
  - Prevents brute force attacks
  - Fair to users sharing IP addresses
  - Relatively simple to implement
- **Implementation**:
  - 5 requests per minute per IP as specified in requirements
  - Using slowapi library for rate limiting in FastAPI

## API Design Research

### RESTful Endpoint Patterns
- Follow standard REST conventions for resource-based operations
- Use consistent URL patterns with user_id in path for isolation
- Implement proper HTTP status codes (200, 201, 401, 403, 404, 422)
- Consistent error response format as specified

### Error Handling Strategy
- **Decision**: Use consistent error response format: `{"message": "...", "error_code": "..."}`
- **Rationale**:
  - Enables consistent error handling in frontend
  - Provides clear feedback to users
  - Matches specification requirements
- **Implementation**:
  - Standard error responses across all endpoints
  - Proper HTTP status codes for different error types

## Component Architecture

### Reusable Component Design
- **Decision**: Create reusable UI components with clear responsibilities
- **Rationale**:
  - Improves maintainability
  - Ensures consistent UI/UX
  - Accelerates development
- **Components to implement**:
  - LoginForm: Handles user login with validation
  - SignupForm: Handles user registration with validation
  - TaskCard: Displays individual task with actions
  - TaskList: Renders list of tasks with filtering
  - TaskForm: Handles task creation and editing
  - Navbar: Shows login/logout state and navigation

### State Management Approach
- **Decision**: Use React state hooks for local component state, JWT for authentication state
- **Rationale**:
  - Simpler than external state management libraries for this use case
  - JWT tokens provide authentication state
  - React hooks are standard for local state
- **Considerations**:
  - Use React Context for global state if needed beyond authentication
  - Consider SWR or React Query for server state management

## Integration Points

### Backend API Integration
- **API endpoints**: Follow RESTful conventions as specified in contracts
- **Authentication**: All endpoints require JWT in Authorization header
- **Error handling**: Consistent error responses across all endpoints
- **Data format**: JSON requests and responses

### Frontend Integration
- **Pages**: /login, /signup, /tasks, /tasks/[id] as specified
- **Components**: Reusable components as defined in spec
- **API client**: Centralized client with automatic JWT attachment
- **Routing**: Next.js App Router with protected routes

## Performance Considerations

### Loading States
- **Implementation**: Show loading indicators during API requests
- **Approach**: Use React Suspense and loading.js in App Router
- **Benefits**: Better user experience during network requests

### Caching Strategy
- **Decision**: Implement selective caching for non-sensitive data
- **Approach**: Cache user's own task lists but not individual task details that might change frequently
- **Consideration**: Invalidate cache after mutations

## Testing Strategy

### Backend Testing
- **Unit tests**: Test individual services and utilities
- **Integration tests**: Test API endpoints with database
- **Contract tests**: Validate API compliance with OpenAPI spec

### Frontend Testing
- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test component interactions
- **E2E tests**: Test complete user flows using Playwright

## Conclusion
The research has successfully identified all key technical decisions needed for the implementation. The approach leverages Next.js App Router with Better Auth for frontend authentication, FastAPI with SQLModel for the backend, and PostgreSQL for data storage. The architecture follows security best practices with JWT tokens stored in HttpOnly cookies and proper user isolation enforced at multiple layers.
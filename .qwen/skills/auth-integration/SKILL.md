# auth-integration

## Purpose
When the user needs to integrate authentication across different parts of their application, use this skill to ensure consistent and secure authentication implementation.

## Instructions for Agent
1. Analyze the existing application architecture to identify all areas requiring authentication:
   - Frontend components/pages
   - Backend API routes/endpoints
   - Database access
   - Third-party service integrations
2. Identify the authentication system being used (Better Auth, NextAuth.js, custom, etc.)
3. Implement authentication on the frontend:
   - Set up authentication context/provider
   - Create protected route components
   - Implement login/logout functionality
   - Add authentication state management
   - Create UI for authentication flows
4. Implement authentication on the backend:
   - Create middleware for protecting API routes
   - Implement token verification
   - Set up session management
   - Add authentication to database queries where needed
5. Ensure consistent user data handling:
   - User profile information
   - Permissions and roles
   - Session data synchronization
6. Integrate authentication with the API client:
   - Automatically attach authentication headers
   - Handle token refresh
   - Manage authentication errors
   - Implement proper logout across all services
7. Implement proper error handling for authentication failures
8. Add security measures:
   - Rate limiting for auth endpoints
   - Secure token storage
   - XSS and CSRF protection
9. Test authentication flows across all integrated parts
10. Document the integration for other developers

## Integration Guidelines
- Maintain consistent user experience across all parts of the application
- Ensure authentication state is synchronized between frontend and backend
- Handle token expiration and refresh automatically
- Implement proper fallback mechanisms
- Secure all communication channels
- Log authentication events for monitoring (without sensitive data)

## When to Use
- User needs to connect authentication across frontend and backend
- Integrating auth system with existing application features
- Connecting authentication to API calls and database access
- Implementing comprehensive authentication across a multi-part application
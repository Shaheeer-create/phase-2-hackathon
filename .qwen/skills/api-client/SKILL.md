# api-client

## Purpose
When the user needs to create, modify, or interact with API clients, use this skill to implement robust and efficient API communication.

## Instructions for Agent
1. Identify the API endpoints and methods needed
2. Determine the appropriate HTTP client library based on the environment:
   - Fetch API for modern browsers
   - Axios for broader compatibility and features
   - Native HTTP modules for Node.js
   - Framework-specific clients when appropriate
3. Implement request configuration:
   - Base URL setup
   - Default headers (Content-Type, Authorization, etc.)
   - Request interceptors for authentication/monitoring
   - Response interceptors for error handling
4. Create methods for different HTTP operations:
   - GET requests with proper query parameter handling
   - POST/PUT/PATCH requests with appropriate body formatting
   - DELETE requests with proper confirmation if needed
5. Implement error handling:
   - Network errors
   - HTTP status code errors (4xx, 5xx)
   - Timeout handling
   - Retry mechanisms for appropriate scenarios
6. Add request/response logging for debugging (with sensitive data filtering)
7. Implement caching strategies where appropriate
8. Ensure proper request/response typing for TypeScript projects
9. Handle authentication and token refresh if required
10. Implement proper request cancellation when needed

## Best Practices
- Use environment variables for API URLs and sensitive configuration
- Implement proper request/response validation
- Follow RESTful conventions where applicable
- Handle rate limiting appropriately
- Ensure proper error messages for different failure scenarios
- Implement proper request/response serialization
- Use appropriate timeout values

## When to Use
- User needs to create an API client for their application
- User wants to modify existing API communication
- User needs to integrate with a specific API
- Building API communication layer for a new project
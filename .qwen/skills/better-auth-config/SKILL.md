# better-auth-config

## Purpose
When the user needs to configure or implement authentication using Better Auth, use this skill to set up secure and properly configured authentication.

## Instructions for Agent
1. Analyze the authentication requirements:
   - User registration and login needs
   - Social authentication providers (Google, GitHub, etc.)
   - Session management requirements
   - Role-based access control needs
2. Set up the Better Auth configuration:
   - Install necessary packages
   - Configure database adapter (Prisma, Drizzle, etc.)
   - Define user schema and custom fields if needed
   - Configure email/password authentication
   - Set up social authentication providers
3. Implement authentication endpoints:
   - Login endpoint
   - Registration endpoint
   - Logout endpoint
   - Password reset functionality
   - Email verification if required
4. Configure session management:
   - Session duration and refresh settings
   - Cookie configuration (secure, httpOnly, sameSite)
   - Cross-origin settings if needed
5. Set up authentication middleware/guards:
   - Protect API routes
   - Protect pages/components
   - Implement role-based access control
6. Handle authentication states in the frontend:
   - Session context
   - Loading states
   - Error handling
7. Implement proper security measures:
   - Rate limiting
   - Password strength requirements
   - Secure token handling
8. Configure email service for verification/password reset
9. Set up proper error handling and user feedback
10. Document the authentication flow for the team

## Security Considerations
- Use HTTPS in production
- Properly configure cookies (secure, httpOnly flags)
- Implement CSRF protection
- Sanitize and validate all inputs
- Use strong password requirements
- Implement account lockout mechanisms
- Regular security audits of auth implementation

## When to Use
- User wants to implement Better Auth in their project
- User needs to configure authentication with specific providers
- User requires custom authentication flows
- Setting up secure authentication for a new application
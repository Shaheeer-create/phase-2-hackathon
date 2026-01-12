# jwt-verifier

## Purpose
When the user needs to verify JWT tokens or implement JWT verification logic, use this skill to handle the verification process correctly.

## Instructions for Agent
1. Identify the JWT token that needs verification
2. Determine the algorithm used for signing (HS256, RS256, etc.)
3. Obtain the appropriate secret key or public key for verification
4. Decode the JWT token to access its payload
5. Verify the token signature using the appropriate key
6. Check token expiration (exp) and not-before (nbf) claims
7. Validate any additional claims as required by the application
8. Handle verification errors appropriately:
   - Invalid signature
   - Expired token
   - Token not yet valid
   - Malformed token
9. Return appropriate response based on verification result
10. Provide guidance on secure JWT handling practices

## Security Considerations
- Never log JWT tokens or their contents
- Always verify the signature before trusting token contents
- Validate all claims, especially audience (aud) and issuer (iss)
- Use appropriate algorithms (prefer RS256 over HS256 for distributed systems)
- Implement proper key rotation mechanisms
- Set reasonable expiration times

## When to Use
- User asks to verify a JWT token
- User needs to implement JWT verification in their application
- User wants to validate token claims
- Security review of JWT implementation is needed
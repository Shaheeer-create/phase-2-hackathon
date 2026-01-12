# FastAPI Todo Backend with Authentication

This is a JWT-secured FastAPI backend service for the Todo application. It provides multi-user support with proper authentication, authorization, and user-level access control.

## Features

- JWT-based authentication with Better Auth integration
- Multi-user support with data isolation
- Full CRUD operations for tasks
- Optimistic locking for concurrent edit protection
- Rate limiting on authentication endpoints
- Secure password storage with bcrypt

## Tech Stack

- Python 3.10+
- FastAPI
- SQLModel
- PostgreSQL (Neon Serverless)
- python-jose for JWT handling
- passlib with bcrypt for password hashing

## Setup

### Prerequisites

- Python 3.10+
- PostgreSQL database (using Neon Serverless in this implementation)

### Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Environment Variables

- `DATABASE_URL`: PostgreSQL database URL (Neon Serverless)
- `SECRET_KEY`: Secret key for JWT signing (use a strong random key in production)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token validity duration in minutes (default: 10080 for 7 days)
- `DEBUG`: Enable debug mode (default: False)

## Running the Application

### Development
```bash
uvicorn main:app --reload
```

### Production
```bash
uvicorn main:app --workers 4
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/logout` - Logout and invalidate session

### Tasks
- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `POST /api/{user_id}/tasks` - Create a new task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

### Users
- `GET /api/users/me` - Get current user information

## Security

### Authentication
- All endpoints require valid JWT tokens
- Tokens are stored in HttpOnly cookies to prevent XSS attacks
- Backend verifies tokens using shared secret

### Authorization
- Users can only access their own tasks
- Backend validates that authenticated user matches URL parameter
- Unauthorized requests return 401 or 403 status codes

### Rate Limiting
- Authentication endpoints are rate-limited to 5 attempts per minute per IP
- Helps prevent brute-force attacks
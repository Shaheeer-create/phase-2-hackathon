# Quickstart Guide: FastAPI Todo Backend

## Overview
This guide provides instructions to quickly set up and run the JWT-secured FastAPI todo backend service.

## Prerequisites
- Python 3.10 or higher
- pip package manager
- PostgreSQL-compatible database (Neon Serverless recommended)
- Environment capable of running uvicorn

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi sqlmodel python-jose[cryptography] passlib[bcrypt] python-multipart
pip install uvicorn[standard]  # For development
```

### 4. Environment Configuration
Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=postgresql://username:password@host:port/database_name
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate a strong SECRET_KEY using:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Database Setup
Run the following command to initialize the database tables:

```bash
# This would typically be done through a dedicated script or alembic migrations
python -c "
from sqlmodel import SQLModel, create_engine
from backend.models import Task, User  # Adjust import path as needed

engine = create_engine('your_database_url_here')
SQLModel.metadata.create_all(engine)
"
```

### 6. Run the Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Usage Examples

### Authentication
First, register or login to obtain a JWT token. The token should be included in the Authorization header for all subsequent requests:

```
Authorization: Bearer <your-jwt-token-here>
```

### Example Requests

#### Get all tasks for user ID 1:
```bash
curl -X GET \
  "http://localhost:8000/api/1/tasks" \
  -H "Authorization: Bearer <your-jwt-token>"
```

#### Create a new task:
```bash
curl -X POST \
  "http://localhost:8000/api/1/tasks" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sample task",
    "description": "This is a sample task",
    "priority": "high"
  }'
```

#### Update a task:
```bash
curl -X PUT \
  "http://localhost:8000/api/1/tasks/1" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

#### Toggle task completion:
```bash
curl -X PATCH \
  "http://localhost:8000/api/1/tasks/1/complete" \
  -H "Authorization: Bearer <your-jwt-token>"
```

## Common Issues

### Database Connection Issues
- Verify DATABASE_URL is correctly formatted
- Ensure the database server is running and accessible
- Check firewall settings if connecting remotely

### Authentication Issues
- Verify JWT token is correctly formatted
- Check that token hasn't expired
- Ensure the SECRET_KEY matches between token generation and verification

### CORS Issues (when calling from browser)
Add CORS middleware to your FastAPI app:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Next Steps
1. Implement user registration/login endpoints
2. Add proper error handling
3. Set up automated testing
4. Configure production deployment settings
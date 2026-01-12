# Quickstart Guide: Frontend Setup and Authentication Integration

## Overview
This guide provides instructions to quickly set up and run the authentication-enabled Todo application. The system includes both frontend (Next.js) and backend (FastAPI) components with JWT-based authentication.

## Prerequisites
- Node.js 18+ (for frontend)
- Python 3.10+ (for backend)
- PostgreSQL (or use Neon Serverless PostgreSQL)
- pnpm, npm, or yarn (for frontend package management)

## Backend Setup

### 1. Environment Configuration
Create a `.env` file in the backend root directory:

```env
# Database
DATABASE_URL="postgresql://username:password@localhost:5432/todo_app_dev"

# JWT Configuration
SECRET_KEY="your-super-secret-key-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days in minutes

# Rate Limiting
AUTH_ATTEMPTS_PER_MINUTE=5
```

Generate a secure SECRET_KEY using Python:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Backend Installation
```bash
cd backend
pip install -r requirements.txt
```

### 3. Database Initialization
```bash
# The application will automatically create tables on startup
# Make sure your database server is running and accessible via DATABASE_URL
```

### 4. Run Backend Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`.

## Frontend Setup

### 1. Environment Configuration
Create a `.env.local` file in the frontend root directory:

```env
# Backend API URL
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000/api"

# Better Auth Configuration
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="your-nextauth-secret-key"
```

### 2. Frontend Installation
```bash
cd frontend
npm install
# or
pnpm install
# or
yarn install
```

### 3. Run Frontend Development Server
```bash
cd frontend
npm run dev
# or
pnpm dev
# or
yarn dev
```

The frontend will be available at `http://localhost:3000`.

## API Usage Examples

### Authentication Flow

#### 1. Register a new user:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123",
    "username": "johndoe"
  }'
```

#### 2. Login to get JWT token:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123"
  }'
```

#### 3. Use JWT token to access protected endpoints:
```bash
curl -X GET http://localhost:8000/api/1/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### Frontend Integration

#### 1. Using the API client in Next.js:
```typescript
// src/lib/api.ts
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Automatically include JWT token in requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token'); // or from HttpOnly cookie
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

#### 2. Example component using authentication:
```typescript
// src/components/LoginForm.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '../lib/api';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    try {
      const response = await api.post('/auth/login', {
        email,
        password
      });
      
      // Store the token (preferably in HttpOnly cookie)
      localStorage.setItem('access_token', response.data.access_token);
      
      // Redirect to tasks page
      router.push('/tasks');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Login failed');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="error">{error}</div>}
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      <button type="submit">Login</button>
    </form>
  );
}
```

## Testing the Authentication System

### 1. Unit Tests
Run backend unit tests:
```bash
cd backend
pytest tests/unit/
```

Run frontend unit tests:
```bash
cd frontend
npm test
```

### 2. Integration Tests
Run backend integration tests:
```bash
cd backend
pytest tests/integration/
```

### 3. End-to-End Tests
Run e2e tests (if configured):
```bash
cd frontend
npm run test:e2e
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
1. Implement password reset functionality
2. Add rate limiting to authentication endpoints
3. Set up monitoring and logging
4. Configure production environment variables
5. Implement proper error handling and user feedback
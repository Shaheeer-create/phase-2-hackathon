from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from src.core.config import settings
from src.api.routes import auth, tasks
from src.core.database import engine, get_session
from contextlib import asynccontextmanager
from typing import AsyncGenerator

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager to handle startup and shutdown events.
    """
    # Startup: Create database tables
    print("Initializing database...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database initialized successfully")
    yield
    # Shutdown: Cleanup if needed
    print("Shutting down...")

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],  # Specific origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Allow headers that might be sent with requests
    allow_origin_regex=r"https?://localhost:\d+",
)


# Include API routes
app.include_router(auth.router, prefix=settings.api_prefix, tags=["auth"])
app.include_router(tasks.router, prefix=settings.api_prefix, tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Todo Backend with Authentication"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
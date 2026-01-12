import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from main import app
from src.core.database import get_session
from src.models import User, Task


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_user_and_task(client: TestClient, session):
    # Register a new user
    user_data = {
        "email": "test@example.com",
        "username": "testuser"
    }
    password = "testpassword"

    # For the register endpoint, we need to send the password as a query parameter
    response = client.post("/api/register", json=user_data, params={"password": password})
    assert response.status_code == 200

    # Authenticate and get token
    response = client.post("/api/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    token_data = response.json()
    access_token = token_data["access_token"]

    # Create a task for the user
    headers = {"Authorization": f"Bearer {access_token}"}
    task_data = {
        "title": "Test Task",
        "description": "This is a test task"
    }

    # Get user ID from token (simplified for test)
    user_id = 1  # Assuming first user gets ID 1

    response = client.post(f"/api/{user_id}/tasks", json=task_data, headers=headers)
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == "Test Task"
    assert task["description"] == "This is a test task"
    assert task["completed"] is False
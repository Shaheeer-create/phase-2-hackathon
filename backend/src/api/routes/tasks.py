from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlmodel import Session
from enum import Enum

from src.models.task import Task, TaskCreate, TaskUpdate, TaskRead
from src.models.token import TokenData
from src.services.task_service import get_tasks, get_task, create_task, update_task, delete_task, toggle_task_completion
from src.core.database import get_session
from src.api.deps import get_user_id_from_token

router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[TaskRead])
def read_tasks(
    user_id: int,
    completed: bool = None,
    current_user_id: int = Depends(get_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for a specific user, optionally filtered by completion status.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        completed: Optional filter for completion status
        current_user_id: The ID of the authenticated user (from token)
        session: Database session

    Returns:
        List[TaskRead]: List of tasks for the user
    """
    # Verify that the authenticated user is accessing their own tasks
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    tasks = get_tasks(session, user_id, completed)
    return tasks


@router.get("/{user_id}/tasks/{id}", response_model=TaskRead)
def read_task(
    user_id: int,
    id: int,
    current_user_id: int = Depends(get_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for a specific user.

    Args:
        user_id: The ID of the user
        id: The ID of the task to retrieve
        current_user_id: The ID of the authenticated user (from token)
        session: Database session

    Returns:
        TaskRead: The requested task
    """
    # Verify that the authenticated user is accessing their own tasks
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    task = get_task(session, id, user_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.post("/{user_id}/tasks", response_model=TaskRead)
def create_task_endpoint(
    user_id: int,
    task_data: TaskCreate,
    current_user_id: int = Depends(get_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Create a new task for a specific user.

    Args:
        user_id: The ID of the user creating the task
        task_data: The task data to create
        current_user_id: The ID of the authenticated user (from token)
        session: Database session

    Returns:
        TaskRead: The created task
    """
    try:
        print(f"DEBUG: create_task_endpoint called - user_id: {user_id}, current_user_id: {current_user_id}")
        print(f"DEBUG: task_data: {task_data}")

        # Verify that the authenticated user is creating tasks for themselves
        if current_user_id != user_id:
            print(f"DEBUG: Authorization error - current_user_id ({current_user_id}) != user_id ({user_id})")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create tasks for this user"
            )

        # Validate task data
        if not task_data.title or len(task_data.title.strip()) == 0:
            print(f"DEBUG: Validation error - task title is empty or blank")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Task title is required"
            )

        print(f"DEBUG: About to call create_task with user_id: {user_id}")
        task = create_task(session, task_data, user_id)
        print(f"DEBUG: Task created successfully: {task.id}")
        return task
    except HTTPException as he:
        print(f"DEBUG: HTTPException in create_task_endpoint: {he.detail}")
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the error for debugging
        print(f"DEBUG: Unexpected error in create_task_endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        # Raise a generic error that will be handled by FastAPI
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.put("/{user_id}/tasks/{id}", response_model=TaskRead)
def update_task_endpoint(
    user_id: int,
    id: int,
    task_data: TaskUpdate,
    current_user_id: int = Depends(get_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Update an existing task for a specific user.

    Args:
        user_id: The ID of the user who owns the task
        id: The ID of the task to update
        task_data: The updated task data
        current_user_id: The ID of the authenticated user (from token)
        session: Database session

    Returns:
        TaskRead: The updated task
    """
    # Verify that the authenticated user is updating their own tasks
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    task = update_task(session, id, task_data, user_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.delete("/{user_id}/tasks/{id}")
def delete_task_endpoint(
    user_id: int,
    id: int,
    current_user_id: int = Depends(get_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Delete a task for a specific user.

    Args:
        user_id: The ID of the user who owns the task
        id: The ID of the task to delete
        current_user_id: The ID of the authenticated user (from token)
        session: Database session

    Returns:
        dict: Success message
    """
    # Verify that the authenticated user is deleting their own tasks
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    success = delete_task(session, id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{id}/complete", response_model=TaskRead)
def toggle_task_completion_endpoint(
    user_id: int,
    id: int,
    current_user_id: int = Depends(get_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task for a specific user.

    Args:
        user_id: The ID of the user who owns the task
        id: The ID of the task to toggle
        current_user_id: The ID of the authenticated user (from token)
        session: Database session

    Returns:
        TaskRead: The updated task with toggled completion status
    """
    # Verify that the authenticated user is toggling their own task
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to toggle this task"
        )

    task = toggle_task_completion(session, id, user_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task
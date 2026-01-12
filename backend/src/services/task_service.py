from sqlmodel import Session, select
from typing import List, Optional
from fastapi import HTTPException, status
import json
from datetime import datetime, date
from enum import Enum

from src.models.task import Task, TaskCreate, TaskUpdate
from src.models.user import User


def get_tasks(session: Session, user_id: int, completed: Optional[bool] = None) -> List[Task]:
    """
    Get all tasks for a specific user, optionally filtered by completion status.

    Args:
        session: The database session
        user_id: The ID of the user whose tasks to retrieve
        completed: Optional filter for completion status

    Returns:
        List[Task]: List of tasks for the user
    """
    query = select(Task).where(Task.user_id == user_id)

    if completed is not None:
        query = query.where(Task.completed == completed)

    tasks = session.exec(query).all()

    # Handle date serialization issue - ensure due_date is a string
    for task in tasks:
        if task.due_date and isinstance(task.due_date, date):
            task.due_date = task.due_date.isoformat()

    return tasks


def get_task(session: Session, task_id: int, user_id: int) -> Optional[Task]:
    """
    Get a specific task by ID for a specific user.
    
    Args:
        session: The database session
        task_id: The ID of the task to retrieve
        user_id: The ID of the user who owns the task
    
    Returns:
        Task: The requested task if it exists and belongs to the user
    """
    task = session.get(Task, task_id)
    if task is None or task.user_id != user_id:
        return None
    return task


def create_task(session: Session, task_data: TaskCreate, user_id: int) -> Task:
    """
    Create a new task for a specific user.

    Args:
        session: The database session
        task_data: The task data to create
        user_id: The ID of the user creating the task

    Returns:
        Task: The created task
    """
    try:
        print(f"DEBUG: create_task called - user_id: {user_id}, task_data: {task_data}")

        # Validate that the user exists
        user = session.get(User, user_id)
        if user is None:
            print(f"DEBUG: User not found - user_id: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Serialize tags to JSON string if provided
        tags_json = None
        if task_data.tags:
            try:
                tags_json = json.dumps(task_data.tags)
                print(f"DEBUG: Tags serialized to JSON: {tags_json}")
            except TypeError:
                print(f"DEBUG: Invalid tags format")
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Invalid tags format"
                )

        print(f"DEBUG: Creating task object with data")
        # Create the task object
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            due_time=task_data.due_time,
            priority=task_data.priority.value if isinstance(task_data.priority, Enum) else task_data.priority,
            tags=tags_json,
            user_id=user_id
        )

        print(f"DEBUG: Adding task to session and committing")
        # Add to session and commit
        session.add(db_task)
        session.commit()

        print(f"DEBUG: Refreshing task object")
        # Refresh to get the updated object with generated fields
        session.refresh(db_task)
        print(f"DEBUG: Task refreshed, ID: {db_task.id}")

        # Convert the tags back from JSON string to ensure proper serialization
        if db_task.tags:
            try:
                # Keep as JSON string for database storage but ensure it's valid
                json.loads(db_task.tags)
            except json.JSONDecodeError:
                # If there's an issue with the JSON, set it to None
                print(f"DEBUG: Invalid JSON in tags, setting to None")
                db_task.tags = None
                session.add(db_task)
                session.commit()
                session.refresh(db_task)

        # Handle date serialization issue - ensure due_date is a string
        if db_task.due_date and isinstance(db_task.due_date, date):
            db_task.due_date = db_task.due_date.isoformat()

        print(f"DEBUG: Returning task with ID: {db_task.id}")
        return db_task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        print(f"DEBUG: HTTPException in create_task")
        raise
    except Exception as e:
        # Log the error for debugging
        print(f"DEBUG: Error creating task: {str(e)}")
        import traceback
        traceback.print_exc()
        # Raise a generic error that will be handled by FastAPI
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the task: {str(e)}"
        )


def update_task(session: Session, task_id: int, task_data: TaskUpdate, user_id: int) -> Optional[Task]:
    """
    Update an existing task for a specific user.
    
    Args:
        session: The database session
        task_id: The ID of the task to update
        task_data: The updated task data
        user_id: The ID of the user who owns the task
    
    Returns:
        Task: The updated task if successful
    """
    db_task = session.get(Task, task_id)

    # Check if task exists and belongs to user
    if db_task is None or db_task.user_id != user_id:
        return None

    # Check for concurrent edit using optimistic locking
    if hasattr(task_data, 'version') and task_data.version != db_task.version:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task was updated by another process. Please refresh and try again."
        )

    # Update fields that are provided
    for field, value in task_data.model_dump(exclude_unset=True).items():
        if field == 'tags' and value is not None:
            setattr(db_task, field, json.dumps(value))
        elif field != 'version':  # Don't update version field directly from input
            setattr(db_task, field, value)

    # Increment version for optimistic locking
    db_task.version += 1
    db_task.updated_at = datetime.utcnow()  # Update timestamp

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


def delete_task(session: Session, task_id: int, user_id: int) -> bool:
    """
    Delete a task for a specific user.
    
    Args:
        session: The database session
        task_id: The ID of the task to delete
        user_id: The ID of the user who owns the task
    
    Returns:
        bool: True if the task was deleted, False if it didn't exist or didn't belong to user
    """
    db_task = session.get(Task, task_id)

    # Check if task exists and belongs to user
    if db_task is None or db_task.user_id != user_id:
        return False

    session.delete(db_task)
    session.commit()

    return True


def toggle_task_completion(session: Session, task_id: int, user_id: int) -> Optional[Task]:
    """
    Toggle the completion status of a task for a specific user.
    
    Args:
        session: The database session
        task_id: The ID of the task to toggle
        user_id: The ID of the user who owns the task
    
    Returns:
        Task: The updated task if successful
    """
    db_task = session.get(Task, task_id)

    # Check if task exists and belongs to user
    if db_task is None or db_task.user_id != user_id:
        return None

    # Check for concurrent edit using optimistic locking
    # Get fresh copy from DB to check for concurrent modifications
    current_db_task = session.get(Task, task_id)
    if current_db_task.version != db_task.version:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task was updated by another process. Please refresh and try again."
        )

    # Toggle completion status
    db_task.completed = not db_task.completed
    db_task.version += 1  # Increment version for optimistic locking
    db_task.updated_at = datetime.utcnow()  # Update timestamp

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task
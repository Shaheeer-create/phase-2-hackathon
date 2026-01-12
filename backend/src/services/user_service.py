from typing import Optional
from sqlmodel import Session, select
from fastapi import HTTPException, status

from ..models.user import User, UserPublic


def get_user_by_id(session: Session, user_id: int) -> Optional[UserPublic]:
    """
    Get a user by their ID.
    
    Args:
        session: The database session
        user_id: The ID of the user to retrieve
    
    Returns:
        UserPublic: The user if found, None otherwise
    """
    user = session.get(User, user_id)
    if user is None:
        return None
    
    # Convert to UserPublic model
    return UserPublic(
        id=user.id,
        email=user.email,
        username=user.username,
        email_verified=user.email_verified,
        created_at=user.created_at
    )


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """
    Get a user by their email.
    
    Args:
        session: The database session
        email: The email of the user to retrieve
    
    Returns:
        User: The user if found, None otherwise
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user
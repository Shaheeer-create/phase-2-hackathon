from datetime import timedelta
from sqlmodel import Session
from fastapi import HTTPException, status
from typing import Optional
import json

from src.models.user import User, UserRegistration
from src.models.token import Token
from src.core.security import create_access_token, verify_password, get_password_hash
from src.core.config import settings


def register_user(session: Session, user_data: UserRegistration) -> User:
    """
    Register a new user with the given data.
    
    Args:
        session: The database session
        user_data: The user registration data
    
    Returns:
        User: The created user
    
    Raises:
        HTTPException: If email is already registered
    """
    # Check if user already exists
    existing_user = session.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user


def authenticate_user(session: Session, email: str, password: str) -> User:
    """
    Authenticate a user by email and password.
    
    Args:
        session: The database session
        email: The user's email
        password: The user's password
    
    Returns:
        User: The authenticated user if credentials are valid
    
    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    user = session.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def create_token_for_user(user: User) -> Token:
    """
    Create a JWT token for the authenticated user.
    
    Args:
        user: The authenticated user
    
    Returns:
        Token: The access token with expiration
    """
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email},
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=int(access_token_expires.total_seconds())
    )
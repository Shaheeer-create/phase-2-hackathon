from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlmodel import Session

from src.models.user import UserRegistration, UserLogin
from src.models.token import Token
from src.services.auth_service import register_user, authenticate_user, create_token_for_user
from src.core.database import get_session
from src.api.deps import get_user_id_from_token

router = APIRouter()
security = HTTPBearer()


@router.post("/auth/register", response_model=Token)
def register_new_user(
    user_data: UserRegistration,
    session: Session = Depends(get_session)
):
    """
    Register a new user with email and password.
    
    Args:
        user_data: The user registration data
        session: Database session
    
    Returns:
        Token: Access token for the newly created user
    """
    # Register the user
    user = register_user(session, user_data)
    
    # Create registration token
    token = create_token_for_user(user)
    
    return token


@router.post("/auth/login", response_model=Token)
def login_user(
    user_credentials: UserLogin,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return access token.
    
    Args:
        user_credentials: The user's email and password
        session: Database session
    
    Returns:
        Token: Access token for the authenticated user
    """
    user = authenticate_user(session, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_token_for_user(user)
    return token


@router.post("/auth/logout")
def logout_user(
    current_user_id: int = Depends(get_user_id_from_token)
):
    """
    Logout the current user.
    
    Args:
        current_user_id: The ID of the authenticated user (from token)
    
    Returns:
        dict: Success message
    """
    # In a real implementation, you might want to invalidate the token
    # For now, we just return a success message
    return {"message": "Successfully logged out"}
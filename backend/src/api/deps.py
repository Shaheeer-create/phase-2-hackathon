from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Generator
from sqlmodel import Session

from src.core.database import get_session
from src.core.security import verify_token, TokenData
from src.models.user import User


security = HTTPBearer()


def get_current_user(
    token: str = Depends(security),
    session: Session = Depends(get_session)
):
    """
    Dependency to get the current authenticated user.

    Args:
        token: The HTTP authorization credentials
        session: Database session

    Returns:
        User: The authenticated user

    Raises:
        HTTPException: If the token is invalid or user doesn't exist
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token.credentials)
    if token_data is None:
        raise credentials_exception

    # Query the user from the database
    user = session.get(User, token_data.user_id)
    if user is None:
        raise credentials_exception

    return user


def get_user_id_from_token(
    token: str = Depends(security)
) -> int:
    """
    Dependency to extract user_id from JWT token.

    Args:
        token: The HTTP authorization credentials

    Returns:
        int: The user ID from the token

    Raises:
        HTTPException: If the token is invalid
    """
    print(f"DEBUG: get_user_id_from_token called with token: {token.credentials[:20] if token.credentials else 'None'}...")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token_data = verify_token(token.credentials)
        print(f"DEBUG: Token verification result: {token_data}")

        if token_data is None or token_data.user_id is None:
            print(f"DEBUG: Token validation failed - token_data: {token_data}")
            raise credentials_exception

        print(f"DEBUG: Returning user_id: {token_data.user_id}")
        return token_data.user_id
    except Exception as e:
        print(f"DEBUG: Exception in get_user_id_from_token: {str(e)}")
        import traceback
        traceback.print_exc()
        raise credentials_exception
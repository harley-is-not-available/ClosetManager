"""
Auth API endpoints for the Closet Management Application.
Handles user registration and authentication.
This file implements the POST /api/v1/auth/register and POST /api/v1/auth/login endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.schemas.auth import Token
from backend.schemas.user import UserCreate, UserLogin, UserResponse
from backend.services.auth_service import AuthService

router = APIRouter()


def get_auth_service(db: Session = Depends(get_db)):
    """Dependency to get AuthService instance."""
    return AuthService(db)


@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    service: AuthService = Depends(get_auth_service),
):
    """
    Register a new user.

    Args:
        user_data: User registration data (email, password, full_name)
        service: AuthService instance

    Returns:
        UserResponse: The created user with all fields

    Raises:
        HTTPException: 400 if user already exists or invalid data
    """
    try:
        user = service.register_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=Token)
async def login_user(
    credentials: UserLogin,
    service: AuthService = Depends(get_auth_service),
):
    """
    Authenticate a user and return JWT token.

    Args:
        credentials: User login credentials (email, password)
        service: AuthService instance

    Returns:
        Token: JWT token for authentication

    Raises:
        HTTPException: 401 if authentication fails
    """
    user = service.authenticate_user(credentials)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # In a complete implementation, we would generate a JWT token here
    # For now, we're demonstrating the API structure
    return Token(
        access_token="fake-jwt-token-for-demo",  # This would be generated in real implementation
        token_type="bearer",
    )

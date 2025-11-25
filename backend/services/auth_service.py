"""
AuthService for handling user authentication operations.
This service implements user registration, authentication, and token management.
"""

import hashlib
import secrets
from typing import Optional

from sqlalchemy.orm import Session

from backend.models.user import User as UserModel
from backend.schemas.user import UserCreate, UserLogin, UserResponse


class AuthService:
    """Service class for handling user authentication operations."""

    def __init__(self, db_session: Session):
        """
        Initialize the AuthService with a database session.

        Args:
            db_session: SQLAlchemy database session
        """
        self.db_session = db_session

    def register_user(self, user_data: UserCreate) -> UserResponse:
        """
        Register a new user.

        Args:
            user_data: Data for creating the user

        Returns:
            The created user with all fields
        """
        # Check if user already exists
        existing_user = (
            self.db_session.query(UserModel)
            .filter(UserModel.email == user_data.email)
            .first()
        )

        if existing_user:
            raise ValueError("User with this email already exists")

        # Hash the password
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((user_data.password + salt).encode()).hexdigest()

        # Create the model instance
        db_user = UserModel(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=password_hash,
            salt=salt,
        )

        # Add to session and commit
        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)

        # Convert to schema and return
        return UserResponse.model_validate(db_user)

    def authenticate_user(self, credentials: UserLogin) -> Optional[UserResponse]:
        """
        Authenticate a user with email and password.

        Args:
            credentials: User login credentials

        Returns:
            The user if authentication is successful, None otherwise
        """
        # Find user by email
        db_user = (
            self.db_session.query(UserModel)
            .filter(UserModel.email == credentials.email)
            .first()
        )

        if db_user is None:
            return None

        # Hash the provided password with the stored salt
        password_hash = hashlib.sha256(
            (credentials.password + db_user.salt).encode()
        ).hexdigest()

        # Check if password matches
        if password_hash != db_user.hashed_password:
            return None

        # Return user data (excluding sensitive fields)
        return UserResponse.model_validate(db_user)

    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """
        Get a user by ID.

        Args:
            user_id: ID of the user to retrieve

        Returns:
            The user if found, None otherwise
        """
        db_user = (
            self.db_session.query(UserModel).filter(UserModel.id == user_id).first()
        )

        if db_user is None:
            return None

        return UserResponse.model_validate(db_user)

    def get_current_user(self, user_id: int) -> Optional[UserResponse]:
        """
        Get the current user by ID (alias for get_user_by_id).

        Args:
            user_id: ID of the user to retrieve

        Returns:
            The user if found, None otherwise
        """
        return self.get_user_by_id(user_id)

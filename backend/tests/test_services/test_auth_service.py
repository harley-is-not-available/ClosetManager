"""
Tests for the AuthService implementation.
These tests follow the same patterns as the item service tests.
"""

import pytest
from pydantic import ValidationError
from sqlalchemy.orm import Session

from backend.models.user import User as UserModel
from backend.schemas.user import UserCreate, UserLogin
from backend.services.auth_service import AuthService


class TestAuthServiceRegistration:
    """Tests for user registration functionality."""

    def test_register_user_success(self, db_session: Session):
        """Test successful user registration."""
        auth_service = AuthService(db_session)

        user_data = UserCreate(
            email="test@example.com", password="password123", full_name="Test User"
        )

        result = auth_service.register_user(user_data)

        assert result.email == user_data.email
        assert result.full_name == user_data.full_name
        assert result.id is not None
        assert result.created_at is not None
        assert result.updated_at is not None

    def test_register_user_duplicate_email_raises_error(self, db_session: Session):
        """Test that registering a user with duplicate email raises an error."""
        auth_service = AuthService(db_session)

        # First registration
        user_data = UserCreate(
            email="test@example.com", password="password123", full_name="Test User"
        )
        auth_service.register_user(user_data)

        # Second registration with same email
        with pytest.raises(ValueError, match="User with this email already exists"):
            auth_service.register_user(user_data)

    def test_register_user_password_hashing(self, db_session: Session):
        """Test that passwords are properly hashed during registration."""
        auth_service = AuthService(db_session)

        user_data = UserCreate(
            email="test2@example.com", password="password123", full_name="Test User 2"
        )

        auth_service.register_user(user_data)

        # Verify that the password is stored as a hash (not plain text)
        # We can't directly verify the hash without accessing the model,
        # but we can verify the user can be authenticated
        login_data = UserLogin(email=user_data.email, password=user_data.password)

        authenticated_user = auth_service.authenticate_user(login_data)
        assert authenticated_user is not None
        assert authenticated_user.email == user_data.email

    def test_register_user_db_storage(self, db_session: Session):
        """Test that cryptographic fields are properly stored in the database."""
        auth_service = AuthService(db_session)
        user_data = UserCreate(email="storage@test.com", password="pwd", full_name="X")
        result = auth_service.register_user(user_data)

        # Access the underlying model directly from the database
        db_model = db_session.query(UserModel).filter(UserModel.id == result.id).one()

        # Assert cryptographic fields are populated
        assert db_model.hashed_password is not None
        assert len(db_model.hashed_password) > 10  # SHA256 is 64 hex chars
        assert db_model.salt is not None
        assert len(db_model.salt) > 10  # secrets.token_hex(16) is 32 hex chars


class TestAuthServiceAuthentication:
    """Tests for user authentication functionality."""

    def test_authenticate_user_success(self, db_session: Session):
        """Test successful user authentication."""
        auth_service = AuthService(db_session)

        # Register a user first
        user_data = UserCreate(
            email="auth@example.com", password="password123", full_name="Auth User"
        )
        auth_service.register_user(user_data)

        # Authenticate the user
        login_data = UserLogin(email=user_data.email, password=user_data.password)

        result = auth_service.authenticate_user(login_data)

        assert result is not None
        assert result.email == user_data.email
        assert result.full_name == user_data.full_name

    def test_authenticate_user_invalid_password(self, db_session: Session):
        """Test authentication with invalid password."""
        auth_service = AuthService(db_session)

        # Register a user first
        user_data = UserCreate(
            email="auth2@example.com", password="password123", full_name="Auth User 2"
        )
        auth_service.register_user(user_data)

        # Try to authenticate with wrong password
        login_data = UserLogin(email=user_data.email, password="wrongpassword")

        result = auth_service.authenticate_user(login_data)

        assert result is None

    def test_authenticate_user_nonexistent_user(self, db_session: Session):
        """Test authentication for non-existent user."""
        auth_service = AuthService(db_session)

        login_data = UserLogin(email="nonexistent@example.com", password="password123")

        result = auth_service.authenticate_user(login_data)

        assert result is None


class TestAuthServiceTokenManagement:
    """Tests for token management functionality."""

    def test_get_user_by_id_existing_user(self, db_session: Session):
        """Test getting user by ID for existing user."""
        auth_service = AuthService(db_session)

        # Register a user first
        user_data = UserCreate(
            email="getuser@example.com", password="password123", full_name="Get User"
        )
        created_user = auth_service.register_user(user_data)

        # Get user by ID
        result = auth_service.get_user_by_id(created_user.id)

        assert result is not None
        assert result.id == created_user.id
        assert result.email == user_data.email

    def test_get_user_by_id_nonexistent_user(self, db_session: Session):
        """Test getting user by ID for non-existent user."""
        auth_service = AuthService(db_session)

        result = auth_service.get_user_by_id(99999)

        assert result is None

    def test_get_current_user_alias(self, db_session: Session):
        """Test that get_current_user is an alias for get_user_by_id."""
        auth_service = AuthService(db_session)

        # Register a user first
        user_data = UserCreate(
            email="currentuser@example.com",
            password="password123",
            full_name="Current User",
        )
        created_user = auth_service.register_user(user_data)

        # Both methods should return the same result
        result1 = auth_service.get_user_by_id(created_user.id)
        result2 = auth_service.get_current_user(created_user.id)

        assert result1 is not None
        assert result2 is not None
        assert result1.id == result2.id
        assert result1.email == result2.email

    def test_get_user_by_id_excludes_sensitive_fields(self, db_session: Session):
        """Test that sensitive fields are excluded from UserResponse."""
        auth_service = AuthService(db_session)

        # Register a user first
        user_data = UserCreate(
            email="sensitive@test.com", password="password123", full_name="Test User"
        )
        created_user = auth_service.register_user(user_data)

        # Get user by ID
        result = auth_service.get_user_by_id(created_user.id)

        # Assert that sensitive attributes are NOT present in the response
        assert not hasattr(result, "hashed_password")
        assert not hasattr(result, "salt")


class TestAuthServiceDatabaseConnection:
    """Tests for database connection handling."""

    def test_service_initialization_with_session(self, db_session: Session):
        """Test that service initializes correctly with a database session."""
        auth_service = AuthService(db_session)

        assert auth_service.db_session == db_session

    def test_service_methods_exist_and_are_callable(self, db_session: Session):
        """Test that all required service methods exist and are callable."""
        auth_service = AuthService(db_session)

        assert callable(auth_service.register_user)
        assert callable(auth_service.authenticate_user)
        assert callable(auth_service.get_user_by_id)
        assert callable(auth_service.get_current_user)


class TestAuthServiceErrorConditions:
    """Tests for error conditions and edge cases."""

    def test_register_user_empty_email(self, db_session: Session):
        """Test registering user with empty email."""
        auth_service = AuthService(db_session)

        # Should raise validation error from Pydantic
        with pytest.raises(ValidationError):
            user_data = UserCreate(
                email="", password="password123", full_name="Test User"
            )
            auth_service.register_user(user_data)

    def test_register_user_empty_password(self, db_session: Session):
        """Test registering user with empty password."""
        auth_service = AuthService(db_session)

        # Should raise validation error from Pydantic
        with pytest.raises(ValidationError):
            user_data = UserCreate(
                email="empty@example.com", password="", full_name="Test User"
            )

            result = auth_service.register_user(user_data)
            assert result.email == user_data.email

    def test_get_user_by_id_negative_id(self, db_session: Session):
        """Test getting user with negative ID."""
        auth_service = AuthService(db_session)

        result = auth_service.get_user_by_id(-1)
        assert result is None

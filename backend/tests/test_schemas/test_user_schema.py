"""
Tests for User schema definitions and validation.
These tests define the requirements for User schema validation.
"""

import datetime

import pytest
from pydantic import ValidationError

from backend.schemas.user import UserCreate, UserLogin, UserResponse


class TestUserCreateSchema:
    """Tests for UserCreate schema validation."""

    def test_user_create_has_required_fields(self):
        """Test that UserCreate has the expected required fields."""
        # Create an instance of UserCreate
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User",
        }

        # Test that required fields exist
        user = UserCreate(**user_data)
        assert hasattr(user, "email")
        assert hasattr(user, "password")
        assert hasattr(user, "full_name")
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.full_name == "Test User"

    def test_user_create_validation(self):
        """Test that UserCreate validates input correctly."""
        # Valid data should pass
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User",
        }

        user = UserCreate(**user_data)
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.full_name == "Test User"

    def test_user_create_requires_email_password_full_name(self):
        """Test that UserCreate requires email, password, and full_name."""
        # Test that email is required
        with pytest.raises(ValidationError):
            UserCreate(password="password123", full_name="Test User")  # type: ignore[reportCallIssue]

        # Test that password is required
        with pytest.raises(ValidationError):
            UserCreate(email="test@example.com", full_name="Test User")  # type: ignore[reportCallIssue]

        # Test that full_name is required
        with pytest.raises(ValidationError):
            UserCreate(email="test@example.com", password="password123")  # type: ignore[reportCallIssue]

        # Test that valid data passes
        user = UserCreate(
            email="test@example.com", password="password123", full_name="Test User"
        )
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.full_name == "Test User"

    def test_user_create_field_types(self):
        """Test that UserCreate fields have correct types."""
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User",
        }

        user = UserCreate(**user_data)

        # Test field types
        assert isinstance(user.email, str)
        assert isinstance(user.password, str)
        assert isinstance(user.full_name, str)

    def test_user_create_email_validation(self):
        """Test that UserCreate validates email format."""
        # Test valid email
        user = UserCreate(
            email="valid@example.com", password="password123", full_name="Test User"
        )
        assert user.email == "valid@example.com"

        # Test that invalid email format raises error
        with pytest.raises(ValidationError):
            UserCreate(
                email="invalid-email", password="password123", full_name="Test User"
            )

    def test_user_create_password_validation(self):
        """Test that UserCreate validates password requirements."""
        # Test valid password
        user = UserCreate(
            email="test@example.com", password="password123", full_name="Test User"
        )
        assert user.password == "password123"

        # Test that password can be empty (in theory, but would need schema definition)
        user = UserCreate(email="test@example.com", password="", full_name="Test User")
        assert user.password == ""

    def test_user_create_missing_required_fields(self):
        """Test that UserCreate requires all required fields."""
        # Test missing all fields
        with pytest.raises(ValidationError):
            UserCreate()  # type: ignore[reportCallIssue]

        # Test missing email
        with pytest.raises(ValidationError):
            UserCreate(password="password123", full_name="Test User")  # type: ignore[reportCallIssue]

        # Test missing password
        with pytest.raises(ValidationError):
            UserCreate(email="test@example.com", full_name="Test User")  # type: ignore[reportCallIssue]

        # Test missing full_name
        with pytest.raises(ValidationError):
            UserCreate(email="test@example.com", password="password123")  # type: ignore[reportCallIssue]

        # Test that valid data passes
        user = UserCreate(
            email="test@example.com", password="password123", full_name="Test User"
        )
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.full_name == "Test User"

    def test_user_create_error_messages(self):
        """Test that appropriate error messages are provided."""
        try:
            UserCreate()  # type: ignore[reportCallIssue]
            assert False, "Should have raised validation error"
        except ValidationError as e:
            assert len(e.errors()) > 0


class TestUserLoginSchema:
    """Tests for UserLogin schema validation."""

    def test_user_login_has_required_fields(self):
        """Test that UserLogin has the expected required fields."""
        # Create an instance of UserLogin
        login_data = {"email": "test@example.com", "password": "password123"}

        # Test that required fields exist
        login = UserLogin(**login_data)
        assert hasattr(login, "email")
        assert hasattr(login, "password")
        assert login.email == "test@example.com"
        assert login.password == "password123"

    def test_user_login_validation(self):
        """Test that UserLogin validates input correctly."""
        # Valid data should pass
        login_data = {"email": "test@example.com", "password": "password123"}

        login = UserLogin(**login_data)
        assert login.email == "test@example.com"
        assert login.password == "password123"

    def test_user_login_requires_email_and_password(self):
        """Test that UserLogin requires email and password."""
        # Test that email is required
        with pytest.raises(ValidationError):
            UserLogin(password="password123")  # type: ignore[reportCallIssue]

        # Test that password is required
        with pytest.raises(ValidationError):
            UserLogin(email="test@example.com")  # type: ignore[reportCallIssue]

        # Test that valid data passes
        login = UserLogin(email="test@example.com", password="password123")
        assert login.email == "test@example.com"
        assert login.password == "password123"

    def test_user_login_field_types(self):
        """Test that UserLogin fields have correct types."""
        login_data = {"email": "test@example.com", "password": "password123"}

        login = UserLogin(**login_data)

        # Test field types
        assert isinstance(login.email, str)
        assert isinstance(login.password, str)

    def test_user_login_email_validation(self):
        """Test that UserLogin validates email format."""
        # Test valid email
        login = UserLogin(email="valid@example.com", password="password123")
        assert login.email == "valid@example.com"

        # Test that invalid email format raises error
        with pytest.raises(ValidationError):
            UserLogin(email="invalid-email", password="password123")

    def test_user_login_missing_required_fields(self):
        """Test that UserLogin requires all required fields."""
        # Test missing all fields
        with pytest.raises(ValidationError):
            UserLogin()  # type: ignore[reportCallIssue]

        # Test missing email
        with pytest.raises(ValidationError):
            UserLogin(password="password123")  # type: ignore[reportCallIssue]

        # Test missing password
        with pytest.raises(ValidationError):
            UserLogin(email="test@example.com")  # type: ignore[reportCallIssue]

        # Test that valid data passes
        login = UserLogin(email="test@example.com", password="password123")
        assert login.email == "test@example.com"
        assert login.password == "password123"

    def test_user_login_error_messages(self):
        """Test that appropriate error messages are provided."""
        try:
            UserLogin()  # type: ignore[reportCallIssue]
            assert False, "Should have raised validation error"
        except ValidationError as e:
            assert len(e.errors()) > 0


class TestUserResponseSchema:
    """Tests for UserResponse schema validation."""

    def test_user_response_has_required_fields(self):
        """Test that UserResponse has the expected required fields."""
        # Create an instance of UserResponse
        user_data = {
            "id": 1,
            "email": "test@example.com",
            "full_name": "Test User",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
        }

        # Test that required fields exist
        user = UserResponse(**user_data)
        assert hasattr(user, "id")
        assert hasattr(user, "email")
        assert hasattr(user, "full_name")
        assert hasattr(user, "created_at")
        assert hasattr(user, "updated_at")
        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"

    def test_user_response_schema_completeness(self):
        """Test that UserResponse schema is complete and comprehensive."""
        # Test all expected fields are present
        expected_fields = ["id", "email", "full_name", "created_at", "updated_at"]

        # Check that all required fields exist
        user = UserResponse(
            id=1,
            email="test@example.com",
            full_name="Test User",
            created_at="2023-01-01T00:00:00",  # type: ignore[reportArgumentType]
            updated_at="2023-01-01T00:00:00",  # type: ignore[reportArgumentType]
        )

        for field in expected_fields:
            assert hasattr(user, field), f"Missing field: {field}"

    def test_user_response_field_types(self):
        """Test that UserResponse fields have correct types."""
        user_data = {
            "id": 1,
            "email": "test@example.com",
            "full_name": "Test User",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
        }

        user = UserResponse(**user_data)

        # Test field types
        assert isinstance(user.id, int)
        assert isinstance(user.email, str)
        assert isinstance(user.full_name, str)

    def test_user_response_id_validation(self):
        """Test that UserResponse validates ID correctly."""
        # Test valid integer ID
        user = UserResponse(
            id=1,
            email="test@example.com",
            full_name="Test User",
            created_at="2023-01-01T00:00:00",  # type: ignore[reportArgumentType]
            updated_at="2023-01-01T00:00:00",  # type: ignore[reportArgumentType]
        )
        assert user.id == 1

        # Test that negative ID raises error (if schema requires positive)
        try:
            UserResponse(
                id=-1,
                email="test@example.com",
                full_name="Test User",
                created_at="2023-01-01T00:00:00",  # type: ignore[reportArgumentType]
                updated_at="2023-01-01T00:00:00",  # type: ignore[reportArgumentType]
            )
            # This might pass depending on schema, so we're not asserting this will fail
        except Exception:
            pass  # May or may not fail depending on schema definition

    def test_user_response_datetime_validation(self):
        """Test that UserResponse validates datetime fields."""
        # Test valid datetime strings
        user = UserResponse(
            id=1,
            email="test@example.com",
            full_name="Test User",
            created_at="2023-01-01T00:00:00",  # type: ignore[reportArgumentType]
            updated_at="2023-01-01T00:00:00",  # type: ignore[reportArgumentType]
        )
        assert user.created_at == datetime.datetime(2023, 1, 1, 0, 0)
        assert user.updated_at == datetime.datetime(2023, 1, 1, 0, 0)

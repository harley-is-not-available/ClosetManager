"""
Test cases for the Auth API endpoints.
These tests cover the POST /api/v1/auth/register and POST /api/v1/auth/login endpoints.
"""

from datetime import datetime, timezone
from unittest.mock import Mock, patch

from backend.api.v1.auth import get_auth_service
from backend.schemas.user import UserCreate, UserResponse
from backend.services.auth_service import AuthService


def test_register_user_success(
    override_auth_service, mock_auth_service_instance, override_get_db, client
):
    """
    Test successful user registration with proper mocking.
    """

    # Create mock user data
    user_data = UserCreate(
        email="test@example.com", password="securepassword", full_name="Test User"
    )

    mock_response = UserResponse(
        id=99,
        email="test@example.com",
        full_name="Test User",
        created_at=datetime.now(),  # Use simple datetime for mock
        updated_at=datetime.now(),
    )

    mock_auth_service_instance.register_user.return_value = mock_response

    # Make the request
    response = client.post(
        "/api/v1/auth/register",
        json=user_data.model_dump(),
    )

    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"


def test_register_user_duplicate_email(
    override_auth_service,
    mock_auth_service_instance,
    override_get_db,
    client,
    test_user_a,
):
    """
    Test user registration with existing email.
    """
    # Mock the AuthService to return a ValueError for duplicate email
    mock_auth_service_instance.register_user.side_effect = ValueError(
        "User with this email already exists"
    )

    # Make the request with duplicate email
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": test_user_a.email,  # Duplicate email
            "password": "securepassword",
            "full_name": "New User",
        },
    )

    # Verify the response
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_register_user_invalid_data(
    override_auth_service, mock_auth_service_instance, override_get_db, client
):
    """
    Test user registration with invalid data.
    """
    # Make the request with incomplete data
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "invalid-email"  # Invalid email format
        },
    )

    # Verify the response
    assert response.status_code == 422  # Validation error


def test_login_user_success(
    override_auth_service,
    mock_auth_service_instance,
    override_get_db,
    client,
    test_user_a,
):
    """
    Test successful user login.
    """
    # Mock the AuthService to return a successful authentication result
    mock_auth_service_instance.authenticate_user.return_value = test_user_a

    # Make the request
    response = client.post(
        "/api/v1/auth/login",
        json={"email": test_user_a.email, "password": "testpassword"},
    )

    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    # Note: access_token is a fake token for demo purposes


def test_login_user_invalid_credentials(
    override_auth_service,
    mock_auth_service_instance,
    override_get_db,
    client,
    test_user_a,
):
    """
    Test user login with invalid credentials.
    """
    # Mock the AuthService to return None for invalid credentials
    mock_auth_service_instance.authenticate_user.return_value = None

    # Make the request with invalid credentials
    response = client.post(
        "/api/v1/auth/login",
        json={"email": test_user_a.email, "password": "wrongpassword"},
    )

    # Verify the response
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


def test_login_user_nonexistent_user(
    override_auth_service, mock_auth_service_instance, override_get_db, client
):
    """
    Test user login with non-existent user.
    """
    # Mock the AuthService to return None for non-existent user
    mock_auth_service_instance.authenticate_user.return_value = None

    # Make the request with non-existent email
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nonexistent@example.com", "password": "anypassword"},
    )

    # Verify the response
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


def test_auth_api_structure(
    override_auth_service, mock_auth_service_instance, override_get_db, client
):
    """
    Test that auth endpoints exist and are callable.
    """
    # Test that the register endpoint accepts the expected parameters
    response = client.post("/api/v1/auth/register")
    # Even without proper data, it should be callable and return a proper status code
    assert response.status_code in [400, 422]  # Bad request or validation error

    # Test that the login endpoint accepts the expected parameters
    response = client.post("/api/v1/auth/login")
    # Even without proper data, it should be callable and return a proper status code
    assert response.status_code in [400, 422]  # Bad request or validation error


def test_register_user_empty_email(client, override_get_db, override_auth_service):
    """
    Test user registration with empty email.
    """
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "", "password": "securepassword", "full_name": "New User"},
    )

    assert response.status_code == 422


def test_register_user_empty_password(client, override_get_db, override_auth_service):
    """
    Test user registration with empty password.
    """
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "newuser@example.com", "password": "", "full_name": "New User"},
    )

    assert response.status_code == 422


def test_register_user_empty_fullname(override_auth_service, override_get_db, client):
    """
    Test user registration with empty full name.
    """
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "securepassword",
            "full_name": "",
        },
    )

    assert response.status_code == 422


def test_login_user_empty_email(client, override_get_db, override_auth_service):
    """
    Test user login with empty email.
    """
    response = client.post(
        "/api/v1/auth/login", json={"email": "", "password": "anypassword"}
    )

    assert response.status_code == 422


def test_login_user_empty_password(override_auth_service, override_get_db, client):
    """
    Test user login with empty password.
    """
    response = client.post(
        "/api/v1/auth/login", json={"email": "test@example.com", "password": ""}
    )

    assert response.status_code == 422


def test_register_user_special_characters(
    override_auth_service,
    mock_auth_service_instance,
    override_get_db,
    client,
    test_user_a,
):
    """
    Test user registration with special characters in data.
    """
    # Mock the AuthService to return a successful registration result
    mock_auth_service_instance.register_user.return_value = test_user_a

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "user+tag@example.com",
            "password": "p@ssw0rd!#$%",
            "full_name": "User With Special Chars",
        },
    )

    assert response.status_code == 200


def test_login_user_special_characters(
    override_auth_service,
    mock_auth_service_instance,
    override_get_db,
    client,
    test_user_a,
):
    """
    Test user login with special characters in credentials.
    """
    # Mock the AuthService to return a successful authentication result
    mock_auth_service_instance.authenticate_user.return_value = test_user_a

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "user+tag@example.com", "password": "p@ssw0rd!#$%"},
    )

    assert response.status_code == 200

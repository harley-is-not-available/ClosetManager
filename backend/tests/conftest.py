import os
from datetime import datetime
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from backend.api.v1.auth import get_auth_service
from backend.api.v1.auth import router as auth_router
from backend.api.v1.items import router as items_router
from backend.config.database import Base, get_db
from backend.models.clothing_item import ClothingItem as ClothingItemModel
from backend.models.user import User
from backend.schemas.clothing_item import ClothingItem, ClothingItemCreate
from backend.services.auth_service import AuthService
from backend.services.upload_service import UploadService

# Test database configuration
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "sqlite:///:memory:",
)
TEST_MONGO_URL = os.getenv("TEST_MONGO_URL", "mongodb://localhost:27017/test_closet_db")

# Create test database engine
test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Create test MongoDB client
test_mongo_client = AsyncIOMotorClient(TEST_MONGO_URL)
test_mongo_db = test_mongo_client.test_closet_db


test_app = FastAPI()
test_app.include_router(items_router, prefix="/api/v1/items", tags=["items"])
test_app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for each test"""
    Base.metadata.create_all(bind=test_engine)

    session = TestSessionLocal()

    yield session

    session.close()

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def test_user_a(db_session):
    """
    Fixture that creates a User in the database for tests.
    """

    user = User(
        id=1,
        email="test@example.com",
        full_name="Test User",
        hashed_password="UHHH",
        salt="Test",
    )
    db_session.add(user)
    db_session.commit()
    # The session is often configured to expire/refresh the object
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user_b(db_session):
    """
    Fixture that creates a User in the database for tests.
    """

    user = User(
        id=2,
        email="testb@example.com",
        full_name="Test UserB",
        hashed_password="UHHB",
        salt="Test",
    )
    db_session.add(user)
    db_session.commit()
    # The session is often configured to expire/refresh the object
    db_session.refresh(user)
    return user


@pytest.fixture
def test_clothing_item_partial_a(db_session, test_user_a):
    """
    Fixture that creates a clothing item with some parameters defined in the database for tests.
    Uses test_user_b
    """

    item_data = ClothingItemCreate(  # type: ignore[reportCallIssue]
        name="Test T-Shirt",
        user_id=test_user_a.id,
        description="A test t-shirt",
        category="Tops",
    )

    db_item = ClothingItemModel(**item_data.model_dump())
    db_session.add(db_item)
    db_session.commit()
    # The session is often configured to expire/refresh the object
    db_session.refresh(db_item)
    return ClothingItem.model_validate(db_item)


@pytest.fixture
def test_clothing_item_full_a(db_session, test_user_a):
    """
    Fixture that creates a clothing item with all parameters defined in the database for tests.
    Uses test_user_a
    """

    item_data = ClothingItemCreate(
        name="Test T-Shirt",
        user_id=test_user_a.id,
        description="A test t-shirt",
        category="Tops",
        size="M",
        color="Blue",
        price=29.99,
        purchase_date=datetime.now(),
        image_path="/images/test.jpg",
    )

    db_item = ClothingItemModel(**item_data.model_dump())
    db_session.add(db_item)
    db_session.commit()
    # The session is often configured to expire/refresh the object
    db_session.refresh(db_item)
    return ClothingItem.model_validate(db_item)


@pytest.fixture
def test_clothing_item_partial_b(db_session, test_user_b):
    """
    Fixture that creates a clothing item with some parameters defined in the database for tests.
    Uses test_user_b
    """

    item_data = ClothingItemCreate(  # type: ignore[reportCallIssue]
        name="Test T-Shirt",
        user_id=test_user_b.id,
        description="A test t-shirt",
        category="Tops",
    )

    db_item = ClothingItemModel(**item_data.model_dump())
    db_session.add(db_item)
    db_session.commit()
    # The session is often configured to expire/refresh the object
    db_session.refresh(db_item)
    return ClothingItem.model_validate(db_item)


@pytest.fixture
def test_clothing_item_full_b(db_session, test_user_b):
    """
    Fixture that creates a clothing item with all parameters defined in the database for tests.
    Uses test_user_b
    """

    item_data = ClothingItemCreate(
        name="Test T-Shirt",
        user_id=test_user_b.id,
        description="A test t-shirt",
        category="Tops",
        size="M",
        color="Blue",
        price=29.99,
        purchase_date=datetime.now(),
        image_path="/images/test.jpg",
    )

    db_item = ClothingItemModel(**item_data.model_dump())
    db_session.add(db_item)
    db_session.commit()
    # The session is often configured to expire/refresh the object
    db_session.refresh(db_item)
    return ClothingItem.model_validate(db_item)


@pytest.fixture(scope="function")
def mongo_db():
    """Create a new MongoDB database for each test"""
    return test_mongo_db


@pytest.fixture
def mock_auth_service_instance():
    """
    Fixture that provides a mocked instance of AuthService for modification.
    """
    # Create the mock instance with spec=True for safety
    mock_instance = Mock(spec=AuthService)

    # Yield the instance so the test can configure it (e.g., set return_value)
    yield mock_instance

    # Cleanup (optional, but good practice): reset the mock state after the test
    mock_instance.reset_mock()


@pytest.fixture
def override_auth_service(client, mock_auth_service_instance):
    """
    Fixture that applies the dependency override for AuthService.
    It uses the mock instance provided by mock_auth_service_instance.
    """

    # Define the callable function (the crucial part)
    def mock_get_auth_service_callable():
        return mock_auth_service_instance

    # Apply the override
    client.app.dependency_overrides[get_auth_service] = mock_get_auth_service_callable

    # Yield control back to the test
    yield

    # Cleanup: Remove the override after the test is complete
    client.app.dependency_overrides.pop(get_auth_service, None)


# @pytest.fixture
# def mock_upload_service_instance():
#     """
#     Fixture that provides a mocked instance of UploadService for modification.
#     """
#     # Create the mock instance with spec=True for safety
#     mock_instance = Mock(spec=UploadService)

#     # Yield the instance so the test can configure it (e.g., set return_value)
#     yield mock_instance

#     # Cleanup (optional, but good practice): reset the mock state after the test
#     mock_instance.reset_mock()


# @pytest.fixture
# def override_upload_service(client, mock_upload_service_instance):
#     """
#     Fixture that applies the dependency override for UploadService.
#     It uses the mock instance provided by mock_upload_service_instance.
#     """

#     # Define the callable function (the crucial part)
#     def mock_get_upload_service_callable():
#         return mock_upload_service_instance

#     # Apply the override
#     client.app.dependency_overrides[get_upload_service] = (
#         mock_get_upload_service_callable
#     )

#     # Yield control back to the test
#     yield

#     # Cleanup: Remove the override after the test is complete
#     client.app.dependency_overrides.pop(get_auth_service, None)


@pytest.fixture
def override_get_db(client, db_session):
    """
    Override the get_db dependency to return the test SQLite session.
    """

    # Define a simple function that returns the fixture's session
    def get_test_db():
        yield db_session

    # 1. Apply the override to the FastAPI app
    # You must use the GLOBAL client defined earlier in conftest
    client.app.dependency_overrides[get_db] = get_test_db

    yield

    # 2. Cleanup
    client.app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope="function")
def client():
    """
    Fixture to provide a clean TestClient instance for every test.
    """
    # Create a fresh client for each test to ensure isolation
    with TestClient(test_app) as c:
        yield c

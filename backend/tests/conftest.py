import os
from datetime import datetime

import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.config.database import Base
from backend.models.clothing_item import ClothingItem as ClothingItemModel
from backend.models.user import User
from backend.schemas.clothing_item import ClothingItem, ClothingItemCreate

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

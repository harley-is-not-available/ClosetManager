import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Test database configuration
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://test_user:test_password@localhost:5432/test_closet_db",
)
TEST_MONGO_URL = os.getenv("TEST_MONGO_URL", "mongodb://localhost:27017/test_closet_db")

# Create test database engine
test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base = declarative_base()

# Create test MongoDB client
test_mongo_client = AsyncIOMotorClient(TEST_MONGO_URL)
test_mongo_db = test_mongo_client.test_closet_db


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for each test"""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def mongo_db():
    """Create a new MongoDB database for each test"""
    return test_mongo_db

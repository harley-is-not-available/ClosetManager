"""
Database connection utilities for PostgreSQL and MongoDB.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .settings import settings


def get_database_url():
    if settings.postgresql_url:
        return settings.postgresql_url
    return "postgresql://user:password@localhost:5432/closet_manager"


# PostgreSQL setup
engine = create_engine(
    get_database_url(),
    pool_size=settings.postgresql_pool_size,
    max_overflow=settings.postgresql_max_overflow,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB setup
mongo_client = AsyncIOMotorClient(settings.mongodb_url)
db = mongo_client.closet_db


def get_db():
    """
    Dependency to get database session for PostgreSQL.

    Yields:
        Session: Database session object
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

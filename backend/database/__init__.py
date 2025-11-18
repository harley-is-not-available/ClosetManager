from typing import AsyncGenerator

from asyncpg import create_pool
from motor.motor_asyncio import AsyncIOMotorClient

# PostgreSQL configuration
POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "password",
    "dbname": "closetmanager",
}

# MongoDB configuration
MONGO_CONFIG = {"host": "localhost", "port": 27017, "dbname": "closetmanager"}


async def get_postgres_db() -> AsyncGenerator:
    """Async generator for PostgreSQL database connection pool."""
    connection = await create_pool(**POSTGRES_CONFIG)
    try:
        yield connection
    finally:
        await connection.close()


async def get_mongo_db() -> AsyncGenerator:
    """Async generator for MongoDB client connection."""
    client = AsyncIOMotorClient(
        f"mongodb://{MONGO_CONFIG['host']}:{MONGO_CONFIG['port']}"
    )
    db = client[MONGO_CONFIG["dbname"]]
    try:
        yield db
    finally:
        client.close()

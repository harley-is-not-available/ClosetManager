import os

import asyncpg


class PostgreSQLDatabase:
    def __init__(self):
        self._pool = None
        self._database_url = os.environ.get("DATABASE_URL")
        if not self._database_url:
            raise ValueError("DATABASE_URL environment variable not set")

    async def setup(self):
        """Initialize the PostgreSQL connection pool."""
        try:
            self._pool = await asyncpg.create_pool(
                self._database_url, min_size=1, max_size=10, command_timeout=30
            )
            # Test connection with a simple query
            async with self._pool.acquire() as conn:
                await conn.execute("SELECT 1")
            print("✅ PostgreSQL connection established successfully")
        except Exception as e:
            print(f"❌ PostgreSQL connection failed: {str(e)}")
            raise

    async def fetch(self, query: str, *params):
        """Execute a query and return results."""
        if not self._pool:
            await self.setup()

        async with self._pool.acquire() as conn:
            async with conn.transaction():
                return await conn.fetch(query, *params)

    async def execute(self, query: str, *params):
        """Execute a query that doesn't return results."""
        if not self._pool:
            await self.setup()

        async with self._pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, *params)

    async def close(self):
        """Properly shut down the connection pool."""
        if self._pool:
            await self._pool.close()
            print("🔒 PostgreSQL connection pool closed")

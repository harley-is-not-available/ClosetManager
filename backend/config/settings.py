"""
Database configuration settings.
"""

from typing import Optional

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Database settings for PostgreSQL and MongoDB connections."""

    # PostgreSQL settings
    postgresql_url: Optional[str] = Field(
        default=None,
        alias="POSTGRES_URL",
        description="PostgreSQL database connection URL",
    )

    # MongoDB settings
    mongodb_url: Optional[str] = Field(
        default=None, alias="MONGODB_URL", description="MongoDB database connection URL"
    )

    # Database settings
    postgresql_pool_size: int = Field(
        default=5,
        alias="POSTGRES_POOL_SIZE",
        description="PostgreSQL connection pool size",
    )

    postgresql_max_overflow: int = Field(
        default=10,
        alias="POSTGRES_MAX_OVERFLOW",
        description="PostgreSQL maximum overflow connections",
    )

    model_config = ConfigDict(  # type: ignore[reportCallIssue]
        env_file=".env",
        case_sensitive=False,
    )


# Global settings instance
settings = DatabaseSettings()

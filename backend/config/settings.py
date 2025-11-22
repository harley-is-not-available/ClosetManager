import os

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database configuration
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/closet_manager"
    )

    # CORS settings
    ALLOWED_ORIGINS: list = Field(default=["*"])

    # JWT settings
    SECRET_KEY: str = Field(default="your-secret-key-here")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)

    # Application settings
    APP_NAME: str = Field(default="Closet Manager")
    VERSION: str = Field(default="1.0.0")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create settings instance
settings = Settings()

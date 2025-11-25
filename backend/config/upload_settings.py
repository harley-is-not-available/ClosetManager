"""
Upload configuration settings.
"""

from typing import Optional

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class UploadSettings(BaseSettings):
    """Upload settings for file storage configuration."""

    # Upload directory setting
    upload_dir: str = Field(
        default="uploads",
        alias="UPLOAD_DIR",
        description="Directory path for storing uploaded files",
    )

    # Use ConfigDict instead of class-based config (recommended for Pydantic v2)
    model_config = ConfigDict(  # type: ignore[reportCallIssue]
        env_file=".env",
        case_sensitive=False,
    )


# Global settings instance
upload_settings = UploadSettings()

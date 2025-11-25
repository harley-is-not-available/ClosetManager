"""
Schema definitions for User models.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_serializer
from pydantic.config import ConfigDict


class UserCreate(BaseModel):
    """
    Schema for creating a new User.
    This schema is used for user registration API requests.
    """

    model_config = ConfigDict(
        # The key is 'from_attributes' (the new name for orm_mode)
        from_attributes=True
    )

    # Required fields
    email: EmailStr = Field(..., description="Email address of the user", min_length=1)
    password: str = Field(
        ..., description="Password for the user account", min_length=1
    )
    full_name: str = Field(..., description="Full name of the user", min_length=1)


class UserLogin(BaseModel):
    """
    Schema for user login.
    This schema is used for user authentication API requests.
    """

    model_config = ConfigDict(
        # The key is 'from_attributes' (the new name for orm_mode)
        from_attributes=True
    )

    # Required fields
    email: EmailStr = Field(..., description="Email address of the user", min_length=1)
    password: str = Field(
        ..., description="Password for the user account", min_length=1
    )


class UserResponse(BaseModel):
    """
    Schema for representing a User in responses.
    This schema includes all fields including ID and timestamps.
    """

    model_config = ConfigDict(
        # The key is 'from_attributes' (the new name for orm_mode)
        from_attributes=True
    )

    # Required fields
    id: int = Field(..., description="Unique identifier for the user")
    email: EmailStr = Field(..., description="Email address of the user")
    full_name: str = Field(..., description="Full name of the user")

    # Timestamps
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: datetime = Field(..., description="Timestamp when the user was created")

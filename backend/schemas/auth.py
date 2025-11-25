"""
Schema definitions for authentication models.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class Token(BaseModel):
    """
    Schema for authentication token response.
    This schema is used for API responses containing authentication tokens.
    """

    model_config = ConfigDict(
        # The key is 'from_attributes' (the new name for orm_mode)
        from_attributes=True
    )

    access_token: str = Field(..., description="Access token for authentication")
    token_type: str = Field(..., description="Type of the token (e.g., 'bearer')")


class TokenData(BaseModel):
    """
    Schema for token payload data.
    This schema contains the data extracted from the authentication token.
    """

    model_config = ConfigDict(
        # The key is 'from_attributes' (the new name for orm_mode)
        from_attributes=True
    )

    user_id: Optional[int] = Field(None, description="ID of the user")
    email: Optional[str] = Field(None, description="Email of the user")

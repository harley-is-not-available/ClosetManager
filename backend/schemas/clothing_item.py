"""
Schema definitions for ClothingItem models.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class ClothingItemCreate(BaseModel):
    """
    Schema for creating a new ClothingItem.
    This schema is used for API requests when creating new clothing items.
    """

    model_config = ConfigDict(
        # The key is 'from_attributes' (the new name for orm_mode)
        from_attributes=True
    )

    # Required fields
    name: str = Field(..., description="Name of the clothing item")
    user_id: int = Field(..., description="ID of the user who owns this item")

    # Optional fields
    description: Optional[str] = Field(
        None, description="Description of the clothing item"
    )
    category: Optional[str] = Field(None, description="Category of the clothing item")
    size: Optional[str] = Field(None, description="Size of the clothing item")
    color: Optional[str] = Field(None, description="Color of the clothing item")
    price: Optional[float] = Field(None, description="Price of the clothing item", ge=0)
    purchase_date: Optional[datetime] = Field(
        None, description="Date when the item was purchased"
    )
    image_path: Optional[str] = Field(
        None, description="Path to the image of the clothing item"
    )


class ClothingItem(ClothingItemCreate):
    """
    Schema for representing a complete ClothingItem.
    This schema includes all fields including the ID and timestamps.
    """

    model_config = ConfigDict(
        # The key is 'from_attributes' (the new name for orm_mode)
        from_attributes=True
    )

    # Required fields (inherited from ClothingItemCreate)
    id: int = Field(..., description="Unique identifier for the clothing item")

    # Timestamps (inherited from base model)
    created_at: datetime = Field(..., description="Timestamp when the item was created")
    updated_at: datetime = Field(
        ..., description="Timestamp when the item was last updated"
    )

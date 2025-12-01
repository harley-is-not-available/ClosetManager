"""
Schema definitions for ClothingItem models.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from backend.models.clothing_item_model import ClothingItemModel


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
    image_data: Optional[str] = Field(None, description="Image Data in base 64")
    image_name: Optional[str] = Field(
        None,
        description="Name of the original image file, only populated on initial create",
    )

    def to_model(
        self, image_data: Optional[str] = None, image_name: Optional[str] = None
    ):
        return {
            "name": self.name,
            "user_id": self.user_id,
            "description": self.description,
            "category": self.category,
            "size": self.size,
            "color": self.color,
            "price": self.price,
            "purchase_date": self.purchase_date,
            "image_path": image_data,
        }


class ClothingItem(ClothingItemCreate):
    """
    Schema for representing a complete ClothingItem.
    This schema includes all fields including the ID and timestamps.
    """

    @classmethod
    def from_model(cls, model: ClothingItemModel, image_data: str):
        """
        Createa a Clothing Item from it's model.
        This will not populate the image_data field. That has to be done externally.
        """
        item = ClothingItem.model_validate(model)
        item.image_data = image_data
        return item

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

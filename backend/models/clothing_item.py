"""
ClothingItem model for the Closet Management Application.
"""

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship

from .abstract_base_model import AbstractBaseModel


class ClothingItem(AbstractBaseModel):
    """
    ClothingItem model representing individual clothing items.
    """

    __tablename__ = "clothing_items"

    # Primary key
    id = mapped_column(Integer, primary_key=True, index=True)

    # Fields
    name = mapped_column(String(255), nullable=False)
    description = mapped_column(Text, nullable=True)
    category = mapped_column(String(100), nullable=True)
    size = mapped_column(String(20), nullable=True)
    color = mapped_column(String(50), nullable=True)
    price = mapped_column(Float, nullable=True)
    purchase_date = mapped_column(DateTime, nullable=True)
    image_path = mapped_column(String(500), nullable=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="clothing_items", lazy="select")

    def __repr__(self) -> str:
        """
        String representation of the ClothingItem instance.

        Returns:
            str: String representation of the ClothingItem
        """
        return f"<ClothingItem(id={getattr(self, 'id', 'N/A')}, name='{getattr(self, 'name', 'N/A')}')>"

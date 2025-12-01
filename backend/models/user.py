"""
User model for the Closet Management Application.
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, relationship

from .abstract_base_model import AbstractBaseModel


class User(AbstractBaseModel):
    """
    User model representing application users.
    """

    __tablename__ = "users"

    # Primary key
    id = mapped_column(Integer, primary_key=True, index=True)

    # Fields
    email = mapped_column(String(255), nullable=False, unique=True)
    hashed_password = mapped_column(String(255), nullable=False)
    salt = mapped_column(String(255), nullable=False)
    full_name = mapped_column(String(255), nullable=False)

    # Relationships
    clothing_items = relationship(
        "ClothingItemModel", back_populates="user", lazy="select"
    )

    def __repr__(self) -> str:
        """
        String representation of the User instance.

        Returns:
            str: String representation of the User
        """
        return f"<User(id={getattr(self, 'id', 'N/A')}, email='{getattr(self, 'email', 'N/A')}')>"

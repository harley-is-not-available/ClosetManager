"""
Base model class for all database models.
This class provides common functionality and fields for all models.
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base

# Create the SQLAlchemy base class
Base = declarative_base()


class AbstractBaseModel(Base):
    """
    Base class for all models to inherit from.
    Provides common fields and methods for database models.
    """

    __abstract__ = True  # This tells SQLAlchemy this is an abstract base class

    # Common fields that all models should have
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    def to_dict(self) -> dict:
        """
        Convert model instance to dictionary representation.

        Returns:
            dict: Dictionary representation of the model instance
        """
        result = {}
        # Only attempt to access __table__ if the instance has been properly initialized
        if hasattr(self, "__table__"):
            for column in self.__table__.columns:
                value = getattr(self, column.name)
                # Handle datetime objects
                if isinstance(value, datetime):
                    value = value.isoformat()
                result[column.name] = value
        return result

    def __repr__(self) -> str:
        """
        String representation of the model instance.

        Returns:
            str: String representation of the model
        """
        return f"<{self.__class__.__name__}(id={getattr(self, 'id', 'N/A')})>"

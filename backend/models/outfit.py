from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from sqlalchemy import ARRAY, Boolean, Column, DateTime, String, Text
from sqlalchemy import UUID as SQL_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Base class for SQLAlchemy models
Base = declarative_base()


# Base model with common fields
class BaseItem(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# SQLAlchemy Outfit model
class Outfit(Base):
    __tablename__ = "outfits"

    id = Column(SQL_UUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    items = Column(ARRAY(SQL_UUID), nullable=True, default=[])
    metadata = Column(String, nullable=True)  # JSON string for outfit metadata
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# Outfit model for API
class OutfitModel(BaseItem):
    name: str
    description: Optional[str] = None
    items: Optional[List[UUID]] = []
    metadata: Optional[str] = None
    is_public: bool = False

    class Config:
        from_attributes = True


# Outfit creation schema
class OutfitCreate(BaseModel):
    name: str
    description: Optional[str] = None
    items: Optional[List[UUID]] = []
    metadata: Optional[str] = None
    is_public: bool = False


# Outfit update schema
class OutfitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    items: Optional[List[UUID]] = []
    metadata: Optional[str] = None
    is_public: Optional[bool] = None

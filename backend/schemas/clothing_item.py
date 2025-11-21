from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# Clothing item creation schema
class ClothingItemCreate(BaseModel):
    brand: Optional[str] = None
    category: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    material: Optional[str] = None
    purchase_date: Optional[datetime] = None
    purchase_price: Optional[str] = None
    condition: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[List[str]] = []
    seasons: Optional[List[str]] = []
    collection_ids: Optional[List[UUID]] = []


# Clothing item update schema
class ClothingItemUpdate(BaseModel):
    brand: Optional[str] = None
    category: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    material: Optional[str] = None
    purchase_date: Optional[datetime] = None
    purchase_price: Optional[str] = None
    condition: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[List[str]] = []
    seasons: Optional[List[str]] = []
    collection_ids: Optional[List[UUID]] = []

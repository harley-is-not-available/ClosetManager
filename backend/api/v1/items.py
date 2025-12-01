"""
Items API endpoints for the Closet Management Application.
Handles CRUD operations for clothing items.
This file implements the GET /api/v1/items, GET /api/v1/items/{id},
POST /api/v1/items, PUT /api/v1/items/{id}, and DELETE /api/v1/items/{id} endpoints.
"""

import base64
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.schemas.clothing_item import ClothingItem, ClothingItemCreate
from backend.services.item_service import ItemService

router = APIRouter()


def get_item_service(db: Session = Depends(get_db)):
    """Dependency to get ItemService instance."""
    return ItemService(db)


@router.get("/", response_model=List[ClothingItem])
async def get_items(
    user_id: int,
    service: ItemService = Depends(get_item_service),
):
    """
    Get all clothing items for a user.

    Args:
        user_id: ID of the user requesting items
        service: ItemService instance

    Returns:
        List of clothing items owned by the user
    """
    items = service.get_all_items(user_id)
    if not items:
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="No items found for this user",
        )
    return items


@router.get("/{item_id}", response_model=ClothingItem)
async def get_item(
    item_id: int,
    user_id: int,
    service: ItemService = Depends(get_item_service),
):
    """
    Get a specific clothing item by ID.

    Args:
        item_id: ID of the clothing item to retrieve
        user_id: ID of the user requesting the item
        service: ItemService instance

    Returns:
        The clothing item if found and owned by user

    Raises:
        HTTPException: 404 if item not found or not owned by user
    """
    item = service.get_item(item_id, user_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or not owned by user",
        )
    return item


@router.post("/", response_model=ClothingItem)
async def create_item(
    item_data: ClothingItemCreate,
    user_id: int,
    service: ItemService = Depends(get_item_service),
):
    """
    Create a new clothing item.

    Args:
        item_data: Data for creating the clothing item
        user_id: ID of the user creating the item
        service: ItemService instance

    Returns:
        The created clothing item with all fields
    """
    item = service.create_item(item_data, user_id)
    return item


@router.put("/{item_id}", response_model=ClothingItem)
async def update_item(
    item_id: int,
    item_data: ClothingItemCreate,
    user_id: int,
    service: ItemService = Depends(get_item_service),
):
    """
    Update a clothing item.

    Args:
        item_id: ID of the clothing item to update
        item_data: Data to update the clothing item with
        user_id: ID of the user requesting the update
        service: ItemService instance
        image_file: Optional image file to upload

    Returns:
        The updated clothing item if found and owned by user

    Raises:
        HTTPException: 404 if item not found or not owned by user
    """

    item = service.update_item(item_id, item_data, user_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or not owned by user",
        )
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    user_id: int,
    service: ItemService = Depends(get_item_service),
):
    """
    Delete a clothing item.

    Args:
        item_id: ID of the clothing item to delete
        user_id: ID of the user requesting the deletion
        service: ItemService instance

    Raises:
        HTTPException: 404 if item not found or not owned by user
    """
    success = service.delete_item(item_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or not owned by user",
        )

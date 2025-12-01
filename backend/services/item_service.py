"""
ItemService for handling clothing item operations.
This service implements CRUD operations for clothing items with proper database integration.
"""

import base64
import os
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from backend.config.upload_settings import upload_settings
from backend.models.clothing_item_model import ClothingItemModel
from backend.schemas.clothing_item import ClothingItem, ClothingItemCreate
from backend.services.upload_service import UploadService


class ItemService:
    """Service class for handling clothing item operations."""

    def __init__(self, db_session: Session):
        """
        Initialize the ItemService with a database session.

        Args:
            db_session: SQLAlchemy database session
        """
        self.db_session = db_session

    def create_item(self, item_data: ClothingItemCreate, user_id: int) -> ClothingItem:
        """
        Create a new clothing item.

        Args:
            item_data: Data for creating the clothing item
            user_id: ID of the user creating the item
            image_data: Optional image file data as bytes
            image_name: Optional name of the image file

        Returns:
            The created clothing item with all fields
        """
        # Create the model instance from the schema data
        data = {**item_data.to_model()}
        data["user_id"] = user_id

        db_item = ClothingItemModel(**data)

        # Add to session and commit
        self.db_session.add(db_item)
        self.db_session.commit()
        self.db_session.refresh(db_item)

        # If image data was provided, upload it using UploadService
        if item_data.image_data is not None and item_data.image_name is not None:
            # Create UploadService instance
            upload_service = UploadService(self.db_session)

            # Upload image and update item with image path
            updated_item = upload_service.upload_image(
                base64.b64decode(item_data.image_data),
                item_data.image_name,
                db_item.id,
                user_id,
            )
            if updated_item:
                # Refresh the item to get updated image path
                self.db_session.refresh(db_item)
                result = ClothingItem.model_validate(db_item)
                result.image_data = item_data.image_data
                return result
            else:
                # If upload fails, return item without image path
                return ClothingItem.model_validate(db_item)
        else:
            # Convert to schema and return
            return ClothingItem.model_validate(db_item)

    def get_item_image(self, item: ClothingItemModel):
        if item.image_path is None:
            return None
        file_path = os.path.join(upload_settings.upload_dir, item.image_path)

        # Read file as bytes and encode to base64
        try:
            with open(file_path, "rb") as f:
                file_bytes = f.read()
            return base64.b64encode(file_bytes).decode("utf-8")
        except FileNotFoundError:
            return None

    def get_item(self, item_id: int, user_id: int) -> Optional[ClothingItem]:
        """
        Get a clothing item by ID.

        Args:
            item_id: ID of the clothing item to retrieve
            user_id: ID of the user requesting the item

        Returns:
            The clothing item if found and owned by user, None otherwise
        """
        db_item = (
            self.db_session.query(ClothingItemModel)
            .filter(ClothingItemModel.id == item_id)
            .filter(ClothingItemModel.user_id == user_id)
            .first()
        )

        if db_item is None:
            return None

        result = ClothingItem.model_validate(db_item)
        result.image_data = self.get_item_image(db_item)
        return result

    def get_all_items(self, user_id: int) -> List[ClothingItem]:
        """
        Get all clothing items.

        Args:
            user_id: ID of the user requesting items (required for ownership enforcement)

        Returns:
            List of clothing items owned by the user
        """
        query = self.db_session.query(ClothingItemModel)

        # Filter by user
        query = query.filter(ClothingItemModel.user_id == user_id)

        db_items = query.all()

        output = []

        for item in db_items:
            output_object = ClothingItem.model_validate(item)
            output_object.image_data = self.get_item_image(item)
            output.append(output_object)

        return output

    def update_item(
        self,
        item_id: int,
        item: ClothingItemCreate,
        user_id: int,
    ) -> Optional[ClothingItem]:
        """
        Update a clothing item.

        Args:
            item_id: ID of the clothing item to update
            item_data: Data to update the clothing item with
            user_id: ID of the user requesting the update (required for ownership enforcement)
            image_data: Optional image file data as bytes
            image_name: Optional name of the image file

        Returns:
            The updated clothing item if found and owned by user, None otherwise
        """
        db_item = (
            self.db_session.query(ClothingItemModel)
            .filter(
                ClothingItemModel.id == item_id, ClothingItemModel.user_id == user_id
            )
            .first()
        )

        if db_item is None:
            return None

        # Update the item fields
        for key, value in item.to_model().items():
            setattr(db_item, key, value)

        self.db_session.commit()
        self.db_session.refresh(db_item)

        # If image data was provided, upload it using UploadService
        if item.image_data is not None and item.image_name is not None:
            # Create UploadService instance
            upload_service = UploadService(self.db_session)

            # Upload image and update item with image path
            updated_item = upload_service.upload_image(
                base64.b64decode(item.image_data),
                item.image_name,
                db_item.id,
                user_id,
            )
            if updated_item:
                # Refresh the item to get updated image path
                self.db_session.refresh(db_item)
                result = ClothingItem.model_validate(db_item)
                result.image_data = item.image_data
                return result
            else:
                # If upload fails, return item without image path
                return ClothingItem.model_validate(db_item)
        else:
            # Convert to schema and return
            return ClothingItem.model_validate(db_item)

    def delete_item(self, item_id: int, user_id: int) -> bool:
        """
        Delete a clothing item.

        Args:
            item_id: ID of the clothing item to delete
            user_id: ID of the user requesting the deletion (required for ownership enforcement)

        Returns:
            True if deletion was successful and item owned by user, False otherwise
        """
        db_item = (
            self.db_session.query(ClothingItemModel)
            .filter(
                ClothingItemModel.id == item_id, ClothingItemModel.user_id == user_id
            )
            .first()
        )

        if db_item is None:
            return False

        self.db_session.delete(db_item)
        self.db_session.commit()
        return True

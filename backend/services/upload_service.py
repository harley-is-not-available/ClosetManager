"""
UploadService for handling image uploads and processing.
This service implements file handling workflows for clothing item images.
"""

import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session

from backend.models.clothing_item import ClothingItem as ClothingItemModel
from backend.schemas.clothing_item import ClothingItem, ClothingItemCreate


class UploadService:
    """Service class for handling image uploads and processing."""

    def __init__(self, db_session: Session, upload_dir: str = "uploads"):
        """
        Initialize the UploadService with a database session and upload directory.

        Args:
            db_session: SQLAlchemy database session
            upload_dir: Directory path for storing uploaded files
        """
        self.db_session = db_session
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)

    def upload_image(
        self, file_path: str, item_id: int, user_id: int
    ) -> Optional[ClothingItem]:
        """
        Upload an image for a clothing item.

        Args:
            file_path: Path to the uploaded file
            item_id: ID of the clothing item to associate the image with
            user_id: ID of the user requesting the upload (for ownership enforcement)

        Returns:
            The updated clothing item if successful, None otherwise
        """
        # Verify the item belongs to the user
        db_item = (
            self.db_session.query(ClothingItemModel)
            .filter(
                ClothingItemModel.id == item_id, ClothingItemModel.user_id == user_id
            )
            .first()
        )

        if db_item is None:
            return None

        # Generate a unique filename using UUID to ensure uniqueness
        file_extension = Path(file_path).suffix
        unique_filename = f"{uuid.uuid4().hex}_{Path(file_path).stem}{file_extension}"
        target_path = self.upload_dir / unique_filename

        try:
            # If there's an existing image, delete it first
            if db_item.image_path:
                old_file_path = Path(db_item.image_path)
                if old_file_path.exists():
                    old_file_path.unlink()

            # Move the file to the upload directory
            shutil.move(file_path, target_path)

            # Update the item with the image path
            db_item.image_path = str(target_path)
            db_item.updated_at = datetime.now()

            # Commit changes
            self.db_session.commit()
            self.db_session.refresh(db_item)

            # Return the updated item
            return ClothingItem.model_validate(db_item)

        except Exception as e:
            # If there's an error, rollback the transaction and return None
            self.db_session.rollback()
            return None

    def delete_image(self, item_id: int, user_id: int) -> bool:
        """
        Delete the image associated with a clothing item.

        Args:
            item_id: ID of the clothing item
            user_id: ID of the user requesting the deletion (for ownership enforcement)

        Returns:
            True if deletion was successful, False otherwise
        """
        # Verify the item belongs to the user
        db_item = (
            self.db_session.query(ClothingItemModel)
            .filter(
                ClothingItemModel.id == item_id, ClothingItemModel.user_id == user_id
            )
            .first()
        )

        if db_item is None or db_item.image_path is None:
            return False

        try:
            # Remove the file from disk
            file_path = Path(db_item.image_path)
            if file_path.exists():
                file_path.unlink()

            # Clear the image path in the database
            db_item.image_path = None
            db_item.updated_at = datetime.now()

            # Commit changes
            self.db_session.commit()
            return True

        except Exception:
            # If there's an error, rollback the transaction
            self.db_session.rollback()
            return False

    def get_upload_directory(self) -> str:
        """
        Get the upload directory path.

        Returns:
            Path to the upload directory
        """
        return str(self.upload_dir)

    def ensure_upload_directory_exists(self) -> bool:
        """
        Ensure the upload directory exists.

        Returns:
            True if directory exists or was created successfully, False otherwise
        """
        try:
            self.upload_dir.mkdir(exist_ok=True)
            return True
        except Exception:
            return False

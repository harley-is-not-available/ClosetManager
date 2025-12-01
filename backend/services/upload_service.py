"""
UploadService for handling image uploads and processing.
This service implements file handling workflows for clothing item images.
"""

import base64
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session

from backend.config.upload_settings import upload_settings
from backend.models.clothing_item_model import ClothingItemModel
from backend.schemas.clothing_item import ClothingItem


class UploadService:
    """Service class for handling image uploads and processing."""

    def __init__(self, db_session: Session):
        """
        Initialize the UploadService with a database session.

        Args:
            db_session: SQLAlchemy database session
        """
        self.db_session = db_session
        self.upload_dir = Path(upload_settings.upload_dir)
        self.upload_dir.mkdir(exist_ok=True)

    def upload_image(
        self, file_data: bytes, file_name: str, item_id: int, user_id: int
    ) -> Optional[ClothingItem]:
        """
        Upload an image for a clothing item.

        Args:
            file_data: Raw bytes of the uploaded file
            file_name: Name of the uploaded file
            item_id: ID of the clothing item to associate the image with
            user_id: ID of the user requesting the upload (for ownership enforcement)

        Returns:
            The updated clothing item if successful, None otherwise
        """
        # Generate a unique filename using UUID to ensure uniqueness
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

        # Check if a file with a different extension already exists for this item
        if db_item.image_path:
            old_file_path = Path(db_item.image_path)
            old_file_extension = old_file_path.suffix
            new_file_extension = Path(file_name).suffix

            if old_file_extension != new_file_extension:
                # Remove the old file if extension differs
                if old_file_path.exists():
                    old_file_path.unlink()

        # Generate a unique filename based on user_id and item_id
        file_extension = Path(file_name).suffix

        if file_extension is None or len(file_extension) == 0:
            return None

        unique_filename = f"{user_id}_{item_id}_{uuid.uuid4().hex}{file_extension}"
        target_path = self.upload_dir / unique_filename

        try:
            # If there's an existing image, delete it first
            if db_item.image_path:
                old_file_path = Path(db_item.image_path)
                if old_file_path.exists():
                    old_file_path.unlink()

            # Save the file to the upload directory
            with open(target_path, "wb") as f:
                f.write(file_data)

            # Update the item with the image path
            db_item.image_path = str(target_path)
            db_item.updated_at = datetime.now()

            # Commit changes
            self.db_session.commit()
            self.db_session.refresh(db_item)

            # Convert the file data to base64 string for the response
            image_data = base64.b64encode(file_data).decode("utf-8")

            # Return the updated item
            return ClothingItem.from_model(db_item, image_data)

        except Exception:
            # If there's an error, rollback the transaction and return None
            self.db_session.rollback()
            return None

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

    # TODO currently untested.
    def delete_image(self, item_id: int, user_id: int) -> bool:
        """
        Delete the image associated with a clothing item.

        Args:
            item_id: ID of the clothing item
            user_id: ID of the user requesting the deletion (for ownership enforcement)

        Returns:
            True if image was deleted successfully, False otherwise
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
            # Delete the file from disk
            file_path = Path(db_item.image_path)
            if file_path.exists():
                file_path.unlink()

            # Clear the image path from the database
            db_item.image_path = None
            db_item.updated_at = datetime.now()

            # Commit changes
            self.db_session.commit()
            self.db_session.refresh(db_item)

            return True
        except Exception:
            # If there's an error, rollback the transaction and return False
            self.db_session.rollback()
            return False

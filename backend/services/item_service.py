"""
ItemService for handling clothing item operations.
This service implements CRUD operations for clothing items with proper database integration.
"""

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from backend.models.clothing_item import ClothingItem as ClothingItemModel
from backend.schemas.clothing_item import ClothingItem, ClothingItemCreate


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

        Returns:
            The created clothing item with all fields
        """
        # Create the model instance from the schema data
        data = {**item_data.model_dump()}
        data["user_id"] = user_id

        db_item = ClothingItemModel(**data)

        # Add to session and commit
        self.db_session.add(db_item)
        self.db_session.commit()
        self.db_session.refresh(db_item)

        # validate and store the object
        result = ClothingItem.model_validate(db_item)

        # Convert to schema and return
        return result

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

        return ClothingItem.model_validate(db_item)

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
        return [ClothingItem.model_validate(item) for item in db_items]

    def update_item(
        self, item_id: int, item_data: dict, user_id: int
    ) -> Optional[ClothingItem]:
        """
        Update a clothing item.

        Args:
            item_id: ID of the clothing item to update
            item_data: Data to update the clothing item with
            user_id: ID of the user requesting the update (required for ownership enforcement)

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

        # Update the item with new data
        for key, value in item_data.items():
            setattr(db_item, key, value)

        # Update timestamps
        db_item.updated_at = datetime.now(timezone.utc)

        # Commit changes
        self.db_session.commit()
        self.db_session.refresh(db_item)

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

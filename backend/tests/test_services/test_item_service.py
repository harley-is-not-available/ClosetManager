"""
Tests for ItemService CRUD operations and database handling.
These tests define the requirements for Subphase 3.1: Item Service Implementation and Tests.
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from backend.schemas.clothing_item import ClothingItem, ClothingItemCreate
from backend.services.item_service import ItemService


class TestItemServiceCRUDOperations:
    """Tests for ItemService CRUD operations."""

    def test_create_clothing_item_comprehensive_fields(self, db_session, test_user_a):
        """Test creating a new clothing item with comprehensive field validation."""
        # Arrange
        item_data = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=test_user_a.id,
            description="A test t-shirt",
            category="Tops",
            size="M",
            color="Blue",
            price=29.99,
            purchase_date=datetime.now(),
            image_path="/images/test.jpg",
        )

        # Act
        service = ItemService(db_session)
        result = service.create_item(item_data, user_id=test_user_a.id)

        # Assert
        # Verify all fields are properly set using the schema field names
        for field_name in ClothingItemCreate.model_fields:
            # Special handling for datetime fields due to precision differences
            if field_name == "purchase_date":
                # For datetime fields, compare with tolerance or as ISO strings
                result_date = getattr(result, field_name)
                original_date = getattr(item_data, field_name)
                # Convert to ISO format for comparison to avoid precision issues
                assert result_date.isoformat() == original_date.isoformat()
            else:
                assert getattr(result, field_name) == getattr(item_data, field_name)

        # Verify the result is the correct type
        assert isinstance(result, ClothingItem)

        # Verify extra fields are present
        assert hasattr(result, "id")
        assert result.id is not None
        assert hasattr(result, "created_at")
        assert result.created_at is not None
        assert hasattr(result, "updated_at")
        assert result.updated_at is not None

    def test_create_clothing_item_minimal_fields(self, db_session, test_user_a):
        """Test creating a clothing item with minimal required fields."""
        # Create the service instance
        service = ItemService(db_session)

        # Create mock data with minimal fields
        item_data = ClothingItemCreate(  # type: ignore[reportCallIssue]
            name="Simple T-Shirt",
            user_id=test_user_a.id,
            description="A simple t-shirt",
        )

        # Test the create method
        result = service.create_item(item_data, user_id=test_user_a.id)

        # Verify all fields are properly set
        assert result.name == "Simple T-Shirt"
        assert result.user_id == test_user_a.id
        assert result.description == "A simple t-shirt"

        # Verify it has required fields
        assert result.id is not None
        assert result.created_at is not None
        assert result.updated_at is not None

    def test_create_item_user_id_enforcement(
        self, db_session, test_user_a, test_user_b
    ):
        """
        Test that the item is created with the user_id provided in the service call
        (the authenticated user), overriding the user_id in the data payload
        (which could be manipulated).
        """
        # Arrange
        service = ItemService(db_session)
        # Payload data claims to be for User B
        item_data = ClothingItemCreate(  # type: ignore[reportCallIssue]
            name="Security Test Item",
            user_id=test_user_b.id,
            description="Should belong to User A.",
        )

        # Act
        # Service call is made in the context of User A
        result = service.create_item(item_data, user_id=test_user_a.id)

        # Assert
        # The resulting item MUST belong to the authenticated user (User A)
        assert result is not None
        assert result.user_id == test_user_a.id
        assert result.user_id != test_user_b.id

        # Verify User B cannot access the item (if get_item is user-scoped)
        assert service.get_item(result.id, user_id=test_user_b.id) is None

    def test_get_clothing_item_by_id_existing_item(
        self, db_session, test_user_a, test_clothing_item_partial_a
    ):
        """Test retrieving an existing clothing item by ID."""
        service = ItemService(db_session)

        # Test the get method
        result = service.get_item(
            test_clothing_item_partial_a.id, user_id=test_user_a.id
        )

        # Verify the result
        assert result is not None
        assert result.id == test_clothing_item_partial_a.id
        assert result.name == "Test T-Shirt"
        assert result.user_id == test_user_a.id

    def test_get_clothing_item_by_id_nonexistent_item(self, db_session, test_user_a):
        """Test retrieving a non-existent clothing item by ID returns None."""
        service = ItemService(db_session)

        # Test that the method returns None for nonexistent item
        result = service.get_item(999, user_id=test_user_a.id)
        assert result is None

    def test_get_all_clothing_items_empty_database(self, db_session, test_user_a):
        """Test retrieving all clothing items when database is empty."""
        service = ItemService(db_session)

        # Test the get all method
        retrieved_items = service.get_all_items(user_id=test_user_a.id)

        # Verify the result is empty list
        assert isinstance(retrieved_items, list)
        assert len(retrieved_items) == 0

    def test_get_all_clothing_items_with_items(
        self,
        db_session,
        test_clothing_item_partial_a,
        test_clothing_item_full_a,
        test_user_a,
    ):
        """Test retrieving all clothing items when items exist."""
        service = ItemService(db_session)

        # Test the get all method
        retrieved_items = service.get_all_items(user_id=test_user_a.id)

        # Verify the result
        assert len(retrieved_items) == 2

        # Create a mapping of expected items by ID for easier verification
        retrieved_dict = {item.id: item for item in retrieved_items}

        # Verify both items are present with correct data
        assert test_clothing_item_partial_a.id in retrieved_dict
        assert test_clothing_item_full_a.id in retrieved_dict

        # Verify partial item data
        partial_item = retrieved_dict[test_clothing_item_partial_a.id]
        assert partial_item.name == test_clothing_item_partial_a.name
        assert partial_item.user_id == test_clothing_item_partial_a.user_id
        assert partial_item.description == test_clothing_item_partial_a.description

        # Verify full item data
        full_item = retrieved_dict[test_clothing_item_full_a.id]
        assert full_item.name == test_clothing_item_full_a.name
        assert full_item.user_id == test_clothing_item_full_a.user_id
        assert full_item.description == test_clothing_item_full_a.description

    def test_update_clothing_item_existing_item(
        self, db_session, test_clothing_item_partial_a, test_user_a
    ):
        """Test updating an existing clothing item."""
        service = ItemService(db_session)

        # Test the update method
        update_data = {
            "name": "Updated T-Shirt",
            "description": "An updated test t-shirt",
        }
        result = service.update_item(
            test_clothing_item_partial_a.id, update_data, user_id=test_user_a.id
        )

        # Verify the result
        assert result is not None
        assert result.name == "Updated T-Shirt"
        assert result.description == "An updated test t-shirt"
        # Verify the updated_at timestamp was updated
        assert result.updated_at is not None
        # Verify created_at is unchanged
        assert result.created_at == test_clothing_item_partial_a.created_at
        # Verify that the item was actually persisted to database
        persisted_item = service.get_item(
            test_clothing_item_partial_a.id, user_id=test_user_a.id
        )
        assert persisted_item is not None
        assert persisted_item.name == "Updated T-Shirt"
        assert persisted_item.description == "An updated test t-shirt"

    def test_update_clothing_item_updated_at_advancement(
        self, db_session, test_clothing_item_partial_a, test_user_a
    ):
        """Test that the 'updated_at' timestamp is strictly advanced after an update."""
        service = ItemService(db_session)

        # Arrange
        original_updated_at = test_clothing_item_partial_a.updated_at

        # Ensure a small time delay (simulating real-world latency) to make comparison meaningful
        # In practice, many ORMs handle this, but an explicit check is safest.
        import time

        time.sleep(0.001)

        update_data = {"name": "Timestamp Check"}

        # Act
        result = service.update_item(
            test_clothing_item_partial_a.id, update_data, user_id=test_user_a.id
        )

        # Assert
        assert result is not None
        # Verify the updated_at time is *later* than the original time
        assert result.updated_at > original_updated_at

    def test_get_clothing_item_by_id_other_user_item(
        self, db_session, test_clothing_item_partial_b, test_user_a
    ):
        """Test retrieving an item belonging to another user returns None."""
        service = ItemService(db_session)

        # Item B belongs to User B. We are simulating a call by User A
        # (or an unauthenticated call that fails to find a matching user_id/item_id).
        # Service should be called with user context to enforce ownership
        result = service.get_item(
            test_clothing_item_partial_b.id, user_id=test_user_a.id
        )

        # Should return None because User A cannot access User B's item
        assert result is None

    def test_get_all_clothing_items_other_user_items(
        self, db_session, test_clothing_item_partial_b, test_user_a
    ):
        """Test that get_all_items only returns items for the requesting user."""
        service = ItemService(db_session)

        # Get all items - should only return User A's items, not User B's
        all_items = service.get_all_items(user_id=test_user_a.id)

        # Verify only User A's items are returned
        for item in all_items:
            assert item.user_id == test_user_a.id

        # Verify User B's item is not returned (this is the key security check)
        user_b_item_ids = [
            item.id
            for item in all_items
            if item.user_id == test_clothing_item_partial_b.user_id
        ]
        assert len(user_b_item_ids) == 0

    def test_update_clothing_item_other_user_item(
        self, db_session, test_clothing_item_partial_b, test_user_a
    ):
        """Test that updating an item belonging to another user returns None."""
        service = ItemService(db_session)

        # Try to update User B's item with User A's permissions
        # Service should be called with user context to enforce ownership
        result = service.update_item(
            test_clothing_item_partial_b.id, {"name": "Hacked"}, user_id=test_user_a.id
        )

        # Should return None because User A cannot update User B's item
        assert result is None

    def test_delete_clothing_item_other_user_item(
        self, db_session, test_clothing_item_partial_b, test_user_a
    ):
        """Test that deleting an item belonging to another user returns False."""
        service = ItemService(db_session)

        # Try to delete User B's item with User A's permissions
        # Service should be called with user context to enforce ownership
        result = service.delete_item(
            test_clothing_item_partial_b.id, user_id=test_user_a.id
        )

        # Should return False because User A cannot delete User B's item
        assert result is False

    def test_update_clothing_item_nonexistent_item(self, db_session, test_user_a):
        """Test updating a non-existent clothing item returns None."""
        service = ItemService(db_session)

        # Test that the method returns None for nonexistent item
        result = service.update_item(999, {"name": "Test"}, user_id=test_user_a.id)
        assert result is None

    def test_update_clothing_item_partial_fields(
        self, db_session, test_clothing_item_full_a, test_user_a
    ):
        """Test updating only some fields of a clothing item."""
        service = ItemService(db_session)

        # Update only some fields
        update_data = {
            "name": "Updated T-Shirt",
        }
        result = service.update_item(
            test_clothing_item_full_a.id, update_data, user_id=test_user_a.id
        )

        # Verify the result
        assert result is not None
        assert result.name == "Updated T-Shirt"
        assert (
            result.description == test_clothing_item_full_a.description
        )  # Should remain unchanged
        assert (
            result.category == test_clothing_item_full_a.category
        )  # Should remain unchanged

    def test_delete_clothing_item_existing_item(
        self, db_session, test_clothing_item_full_a, test_user_a
    ):
        """Test deleting an existing clothing item."""
        service = ItemService(db_session)

        # Assert object exists before delete
        prior_object = service.get_item(
            test_clothing_item_full_a.id, user_id=test_user_a.id
        )
        assert prior_object is not None

        # Test the delete method
        result = service.delete_item(
            test_clothing_item_full_a.id, user_id=test_user_a.id
        )

        # Verify the result
        assert result is True

        # Verify item is actually deleted
        deleted_item = service.get_item(
            test_clothing_item_full_a.id, user_id=test_user_a.id
        )
        assert deleted_item is None

    def test_delete_clothing_item_nonexistent_item(self, db_session, test_user_a):
        """Test deleting a non-existent clothing item returns False."""
        service = ItemService(db_session)

        # Test that the method returns False for nonexistent item
        result = service.delete_item(999, user_id=test_user_a.id)
        assert result is False


class TestItemServiceDatabaseConnection:
    """Tests for database connection handling in ItemService."""

    def test_service_initialization_with_session(self, db_session):
        """Test that ItemService initializes correctly with a database session."""
        service = ItemService(db_session)

        # Verify that the service has the correct session
        assert service.db_session is db_session

    def test_service_methods_exist_and_are_callable(self, db_session):
        """Test that service methods exist and can be called."""
        service = ItemService(db_session)

        # Verify that methods exist and can be called
        assert callable(getattr(service, "create_item"))
        assert callable(getattr(service, "get_item"))
        assert callable(getattr(service, "get_all_items"))
        assert callable(getattr(service, "update_item"))
        assert callable(getattr(service, "delete_item"))


class TestItemServiceErrorConditions:
    """Tests for error conditions in ItemService."""

    def test_get_nonexistent_item_returns_none(self, db_session, test_user_a):
        """Test that getting a non-existent item returns None."""
        service = ItemService(db_session)

        # Test that the method returns None for nonexistent item
        result = service.get_item(999, user_id=test_user_a.id)
        assert result is None

    def test_update_nonexistent_item_returns_none(self, db_session, test_user_a):
        """Test that updating a non-existent item returns None."""
        service = ItemService(db_session)

        # Test that the method returns None for nonexistent item
        result = service.update_item(999, {"name": "Test"}, user_id=test_user_a.id)
        assert result is None

    def test_update_item_with_empty_data(
        self, db_session, test_user_a, test_clothing_item_partial_a
    ):
        """Test updating an item with empty data dictionary."""
        service = ItemService(db_session)

        # Test the update method with empty data
        result = service.update_item(
            test_clothing_item_partial_a.id, {}, user_id=test_user_a.id
        )

        # Should return the item unchanged
        assert result is not None
        assert result.name == test_clothing_item_partial_a.name
        assert result.description == test_clothing_item_partial_a.description

    def test_create_item_with_none_values(self, db_session, test_user_a):
        """Test creating an item with optional None values."""
        service = ItemService(db_session)

        # Create mock data with None values
        item_data = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=test_user_a.id,
            description="A test t-shirt",
            category=None,  # Optional field set to None
            size=None,  # Optional field set to None
            color=None,  # Optional field set to None
            price=None,  # Optional field set to None
            purchase_date=None,  # Optional field set to None
            image_path=None,  # Optional field set to None
        )

        # Test the create method
        result = service.create_item(item_data, user_id=test_user_a.id)

        # Verify the result
        assert result is not None
        assert result.name == "Test T-Shirt"
        assert result.category is None
        assert result.size is None
        assert result.color is None
        assert result.price is None
        assert result.purchase_date is None
        assert result.image_path is None
        # Explicitly test that default values work correctly (for optional fields)
        assert result.purchase_date is None
        assert result.image_path is None

    def test_create_item_with_invalid_price(self, db_session, test_user_a):
        """Test creating an item with invalid price raises validation error."""
        service = ItemService(db_session)

        # Since validation happens at schema level, it should raise ValidationError
        with pytest.raises(ValidationError):
            # Test with negative price (assuming negative prices are not allowed)
            item_data = ClothingItemCreate(  # type: ignore[reportCallIssue]
                name="Test T-Shirt",
                user_id=test_user_a.id,
                description="A test t-shirt",
                price=-5.99,  # Invalid negative price
            )

            service.create_item(item_data, user_id=test_user_a.id)

    def test_create_item_with_invalid_field_types(self, db_session, test_user_a):
        """Test creating an item with invalid field types raises validation error."""
        service = ItemService(db_session)

        # Since validation happens at schema level, it should raise ValidationError
        with pytest.raises(ValidationError):
            item_data = ClothingItemCreate(  # type: ignore[reportCallIssue]
                name="Test T-Shirt",
                user_id=test_user_a.id,
                description="A test t-shirt",
                price="invalid_price",  # Should be numeric
            )

            service.create_item(item_data, user_id=test_user_a.id)

"""
Tests for ClothingItem schema definitions and validation.
These tests define the requirements for Subphase 2.1: Core Schema Definitions and Tests.
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from backend.schemas.clothing_item import ClothingItem, ClothingItemCreate


class TestClothingItemCreateSchema:
    """Tests for ClothingItemCreate schema validation."""

    def test_clothing_item_create_has_required_fields(self):
        """Test that ClothingItemCreate has the expected required fields."""
        # Test that required fields exist using model_fields approach
        assert "name" in ClothingItemCreate.model_fields
        assert "user_id" in ClothingItemCreate.model_fields

        assert ClothingItemCreate.model_fields["name"].is_required()
        assert ClothingItemCreate.model_fields["user_id"].is_required()

    def test_clothing_item_create_optional_fields(self):
        """Test that ClothingItemCreate has optional fields."""
        # Test with optional fields
        item_data = {
            "name": "Test T-Shirt",
            "user_id": 1,
            "description": "A test t-shirt",
            "category": "Tops",
            "size": "M",
            "color": "Blue",
            "price": 29.99,
            "purchase_date": datetime.now(),
            "image_data": "/images/test.jpg",
            "image_name": "test_image.jpg",
        }

        item = ClothingItemCreate(**item_data)

        # Optional fields should be present
        assert "description" in ClothingItemCreate.model_fields
        assert "category" in ClothingItemCreate.model_fields
        assert "size" in ClothingItemCreate.model_fields
        assert "color" in ClothingItemCreate.model_fields
        assert "price" in ClothingItemCreate.model_fields
        assert "purchase_date" in ClothingItemCreate.model_fields
        assert "image_data" in ClothingItemCreate.model_fields
        assert "image_name" in ClothingItemCreate.model_fields

        # Values should be set correctly
        assert item.description == "A test t-shirt"
        assert item.category == "Tops"
        assert item.size == "M"
        assert item.color == "Blue"
        assert item.price == 29.99
        assert item.image_data == "/images/test.jpg"
        assert item.image_name == "test_image.jpg"

    def test_clothing_item_create_validation(self):
        """Test that ClothingItemCreate validates input correctly."""
        # Valid data should pass
        item_data = {"name": "Test T-Shirt", "user_id": 1}

        item = ClothingItemCreate(**item_data)
        assert item.name == "Test T-Shirt"
        assert item.user_id == 1

        # Test with all fields
        item_data_full = {
            "name": "Test T-Shirt",
            "user_id": 1,
            "description": "A test t-shirt",
            "category": "Tops",
            "size": "M",
            "color": "Blue",
            "price": 29.99,
            "purchase_date": datetime.now(),
            "image_data": "/images/test.jpg",
            "image_name": "test_image.jpg",
        }

        item_full = ClothingItemCreate(**item_data_full)
        assert item_full.name == "Test T-Shirt"
        assert item_full.user_id == 1
        assert item_full.description == "A test t-shirt"
        assert item_full.category == "Tops"
        assert item_full.size == "M"
        assert item_full.color == "Blue"
        assert item_full.price == 29.99
        assert item_full.image_data == "/images/test.jpg"
        assert item_full.image_name == "test_image.jpg"

    def test_clothing_item_create_field_types(self):
        """Test that ClothingItemCreate fields have correct types."""
        item_data = {
            "name": "Test T-Shirt",
            "user_id": 1,
            "price": 29.99,
            "size": "M",
            "color": "Blue",
        }

        item = ClothingItemCreate(**item_data)

        # Test field types
        assert isinstance(item.name, str)
        assert isinstance(item.user_id, int)
        assert isinstance(item.price, (int, float))
        assert isinstance(item.size, str)
        assert isinstance(item.color, str)

    def test_clothing_item_create_field_validation(self):
        """Test that ClothingItemCreate validates field values correctly."""
        # Test valid numeric price
        item = ClothingItemCreate(
            name="Test",
            user_id=1,
            price=29.99,
            description=None,
            category=None,
            size=None,
            color=None,
            purchase_date=None,
            image_data=None,
            image_name=None,
        )
        assert item.price == 29.99

        # Test valid integer price
        item = ClothingItemCreate(
            name="Test",
            user_id=1,
            price=50,
            description=None,
            category=None,
            size=None,
            color=None,
            purchase_date=None,
            image_data=None,
            image_name=None,
        )
        assert item.price == 50

        # Test valid size
        item = ClothingItemCreate(
            name="Test",
            user_id=1,
            size="L",
            description=None,
            category=None,
            color=None,
            price=None,
            purchase_date=None,
            image_data=None,
            image_name=None,
        )
        assert item.size == "L"

        # Test valid image_name
        item = ClothingItemCreate(
            name="Test",
            user_id=1,
            image_name="test_image.jpg",
            description=None,
            category=None,
            size=None,
            color=None,
            price=None,
            purchase_date=None,
            image_data=None,
        )
        assert item.image_name == "test_image.jpg"

    def test_clothing_item_create_missing_required_fields(self):
        """Test that ClothingItemCreate requires name and user_id."""
        # Test that name is required
        with pytest.raises(ValidationError):
            ClothingItemCreate(
                user_id=1,
                description=None,
                category=None,
                size=None,
                color=None,
                price=None,
                purchase_date=None,
                image_data=None,
                image_name=None,
            )  # type: ignore[reportCallIssue]

        # Test that user_id is required
        with pytest.raises(ValidationError):
            ClothingItemCreate(
                name="Test T-Shirt",
                description=None,
                category=None,
                size=None,
                color=None,
                price=None,
                purchase_date=None,
                image_data=None,
            )  # type: ignore[reportCallIssue]

        # Test that valid data passes
        item = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description=None,
            category=None,
            size=None,
            color=None,
            price=None,
            purchase_date=None,
            image_data=None,
            image_name=None,
        )
        assert item.name == "Test T-Shirt"
        assert item.user_id == 1

    def test_clothing_item_create_optional_fields_not_required(self):
        """Test that optional fields are not required in ClothingItemCreate."""
        # This should pass even without optional fields
        item = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description=None,
            category=None,
            size=None,
            color=None,
            price=None,
            purchase_date=None,
            image_data=None,
            image_name=None,
        )
        assert item.name == "Test T-Shirt"
        assert item.user_id == 1
        # Optional fields should be None if not provided
        assert item.description is None
        assert item.category is None
        assert item.size is None
        assert item.color is None
        assert item.price is None
        assert item.purchase_date is None
        assert item.image_data is None

    def test_clothing_item_create_max_length_validation(self):
        """Test that ClothingItemCreate validates field length constraints."""
        # Test with maximum allowed string length
        long_name = "A" * 255  # Maximum allowed length
        item = ClothingItemCreate(
            name=long_name,
            user_id=1,
            description=None,
            category=None,
            size=None,
            color=None,
            price=None,
            purchase_date=None,
            image_data=None,
            image_name=None,
        )
        assert item.name == long_name

        # Test with valid lengths for other fields
        item = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            category="Tops",
            size="M",
            color="Blue",
            description=None,
            price=None,
            purchase_date=None,
            image_data=None,
            image_name=None,
        )
        assert item.category == "Tops"
        assert item.size == "M"
        assert item.color == "Blue"


class TestClothingItemSchema:
    """Tests for ClothingItem schema completeness."""

    def test_clothing_item_has_all_fields(self):
        """Test that ClothingItem has all fields including ID and timestamps."""
        # Create an instance with all fields
        item_data = {
            "id": 1,
            "name": "Test T-Shirt",
            "description": "A test t-shirt",
            "category": "Tops",
            "size": "M",
            "color": "Blue",
            "price": 29.99,
            "purchase_date": datetime.now(),
            "image_data": "/images/test.jpg",
            "user_id": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        item = ClothingItem(**item_data)

        # All fields should be present using model_fields approach
        assert "id" in ClothingItem.model_fields
        assert "name" in ClothingItem.model_fields
        assert "description" in ClothingItem.model_fields
        assert "category" in ClothingItem.model_fields
        assert "size" in ClothingItem.model_fields
        assert "color" in ClothingItem.model_fields
        assert "price" in ClothingItem.model_fields
        assert "purchase_date" in ClothingItem.model_fields
        assert "image_data" in ClothingItem.model_fields
        assert "image_name" in ClothingItem.model_fields
        assert "user_id" in ClothingItem.model_fields
        assert "created_at" in ClothingItem.model_fields
        assert "updated_at" in ClothingItem.model_fields

        # Values should be set correctly
        assert item.id == 1
        assert item.name == "Test T-Shirt"
        assert item.description == "A test t-shirt"
        assert item.category == "Tops"
        assert item.size == "M"
        assert item.color == "Blue"
        assert item.price == 29.99
        assert item.user_id == 1

    def test_clothing_item_schema_completeness(self):
        """Test that ClothingItem schema is complete and comprehensive."""
        # Test all expected fields are present using model_fields approach
        expected_fields = [
            "id",
            "name",
            "description",
            "category",
            "size",
            "color",
            "price",
            "purchase_date",
            "image_data",
            "image_name",
            "user_id",
            "created_at",
            "updated_at",
        ]

        # Check that all required fields exist
        item = ClothingItem(
            id=1,
            name="Test T-Shirt",
            user_id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            description=None,
            category=None,
            size=None,
            color=None,
            price=None,
            purchase_date=None,
            image_data=None,
            image_name=None,
        )

        for field in expected_fields:
            assert field in ClothingItem.model_fields, f"Missing field: {field}"

        # Test that all fields have correct types
        assert isinstance(item.id, int)
        assert isinstance(item.name, str)
        assert isinstance(item.user_id, int)
        assert isinstance(item.created_at, datetime)
        assert isinstance(item.updated_at, datetime)

    def test_clothing_item_field_types(self):
        """Test that ClothingItem fields have correct types."""
        item_data = {
            "id": 1,
            "name": "Test T-Shirt",
            "user_id": 1,
            "price": 29.99,
            "size": "M",
            "color": "Blue",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        item = ClothingItem(**item_data)

        # Test field types
        assert isinstance(item.id, int)
        assert isinstance(item.name, str)
        assert isinstance(item.user_id, int)
        assert isinstance(item.price, (int, float))
        assert isinstance(item.size, str)
        assert isinstance(item.color, str)
        assert isinstance(item.created_at, datetime)
        assert isinstance(item.updated_at, datetime)


class TestRequiredFieldEnforcement:
    """Tests for required field enforcement."""

    def test_clothing_item_create_requires_name_and_user_id(self):
        """Test that ClothingItemCreate requires name and user_id."""
        # Test that name is required
        with pytest.raises(ValidationError):
            ClothingItemCreate(
                user_id=1,  # type: ignore[reportCallIssue]
                description=None,
                category=None,
                size=None,
                color=None,
                price=None,
                purchase_date=None,
                image_data=None,
            )

        # Test that user_id is required
        with pytest.raises(ValidationError):
            ClothingItemCreate(
                name="Test T-Shirt",
                description=None,
                category=None,
                size=None,
                color=None,
                price=None,
                purchase_date=None,
                image_data=None,
                image_name=None,
            )  # type: ignore[reportCallIssue]

        # Test that valid data passes
        item = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description=None,
            category=None,
            size=None,
            color=None,
            price=None,
            purchase_date=None,
            image_data=None,
            image_name=None,
        )
        assert item.name == "Test T-Shirt"
        assert item.user_id == 1

    def test_clothing_item_requires_id_for_full_schema(self):
        """Test that ClothingItem requires id for full schema."""
        # Test with minimum required fields for the full schema
        item_data = {
            "id": 1,
            "name": "Test T-Shirt",
            "user_id": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        item = ClothingItem(**item_data)
        assert item.id == 1
        assert item.name == "Test T-Shirt"
        assert item.user_id == 1

    def test_clothing_item_create_optional_fields_not_required(self):
        """Test that optional fields are not required in ClothingItemCreate."""
        # This should pass even without optional fields
        item = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description=None,
            category=None,
            size=None,
            color=None,
            price=None,
            purchase_date=None,
            image_data=None,
            image_name=None,
        )
        assert item.name == "Test T-Shirt"
        assert item.user_id == 1
        # Optional fields should be None if not provided
        assert item.description is None
        assert item.category is None
        assert item.size is None
        assert item.color is None
        assert item.price is None
        assert item.purchase_date is None
        assert item.image_data is None

    def test_clothing_item_create_valid_field_ranges(self):
        """Test that ClothingItemCreate validates field ranges."""
        # Test valid price range
        item = ClothingItemCreate(
            name="Test",
            user_id=1,
            price=0,
            description=None,
            category=None,
            size=None,
            color=None,
            purchase_date=None,
            image_data=None,
            image_name=None,
        )
        assert item.price == 0

        item = ClothingItemCreate(
            name="Test",
            user_id=1,
            price=999999.99,
            description=None,
            category=None,
            size=None,
            color=None,
            purchase_date=None,
            image_data=None,
            image_name=None,
        )
        assert item.price == 999999.99

        # Test valid size
        item = ClothingItemCreate(
            name="Test",
            user_id=1,
            size="XS",
            description=None,
            category=None,
            price=None,
            color=None,
            purchase_date=None,
            image_data=None,
            image_name=None,
        )
        assert item.size == "XS"

        item = ClothingItemCreate(
            name="Test",
            user_id=1,
            size="XXL",
            description=None,
            category=None,
            price=None,
            color=None,
            purchase_date=None,
            image_data=None,
            image_name=None,
        )
        assert item.size == "XXL"

    def test_clothing_item_create_error_messages(self):
        """Test that appropriate error messages are provided."""
        # Test missing required fields
        try:
            ClothingItemCreate()  # type: ignore[reportCallIssue]
            assert False, "Should have raised validation error"
        except ValidationError as e:
            assert len(e.errors()) > 0

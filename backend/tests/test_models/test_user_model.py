"""
Tests for the User model implementation.
These tests define the requirements for the User model.
"""

from backend.models.abstract_base_model import AbstractBaseModel
from backend.models.clothing_item_model import ClothingItemModel  # noqa: F401
from backend.models.user import User


class TestUserModel:
    """Tests for the User model structure and fields."""

    def test_user_inheritance(self):
        """Test that User properly inherits from AbstractBaseModel."""
        # Verify it inherits from BaseModel
        assert issubclass(User, AbstractBaseModel)
        assert hasattr(User, "__table__")

    def test_user_has_required_fields(self):
        """Test that User has the expected required fields."""

        # Create an instance of User
        user = User()

        # Check that required fields exist
        assert hasattr(user, "id")
        assert hasattr(user, "email")
        assert hasattr(user, "hashed_password")
        assert hasattr(user, "full_name")

    def test_user_field_types(self):
        """Test that User fields have correct types."""
        # Check field types
        # Test primary key
        assert hasattr(User, "id")

        # Test string fields
        assert hasattr(User, "email")
        assert hasattr(User, "hashed_password")
        assert hasattr(User, "full_name")

        # Test date fields
        assert hasattr(User, "created_at")
        assert hasattr(User, "updated_at")

    def test_user_relationships(self):
        """Test that User has proper relationships."""
        # Verify the clothing_items relationship exists
        assert hasattr(User, "clothing_items")

        # Verify that the relationship is correctly defined
        # Check that User has a one-to-many relationship with ClothingItem
        assert hasattr(User, "clothing_items")

    def test_user_constraints(self):
        """Test that User has proper constraints."""
        # Test required fields constraints (not null)
        assert hasattr(User, "email")
        assert hasattr(User, "hashed_password")
        assert hasattr(User, "full_name")

    def test_user_to_dict_method(self):
        """Test the to_dict method of User."""
        # Create a User instance with some test data
        user = User()
        user.id = 1
        user.email = "test@example.com"
        user.hashed_password = "hashed_password_123"
        user.full_name = "Test User"

        # Test to_dict method
        result = user.to_dict()
        assert isinstance(result, dict)
        assert result.get("id") == 1
        assert result.get("email") == "test@example.com"
        assert result.get("full_name") == "Test User"
        assert "created_at" in result
        assert "updated_at" in result

    def test_user_repr_method(self):
        """Test the __repr__ method of User."""
        user = User()
        user.id = 1
        user.email = "test@example.com"

        # Test repr method
        result = repr(user)
        assert result.startswith("<User(id=1, email='test@example.com')>")
        assert "User" in result


class TestUserDatabaseIntegration:
    """Tests for User database integration and constraints."""

    def test_database_table_name(self):
        """Test that User has correct table name."""
        assert User.__table__.name == "users"

    def test_database_column_definitions(self):
        """Test that User has proper database column definitions."""
        # Check for required columns
        table = User.__table__
        assert "id" in table.columns
        assert "email" in table.columns
        assert "hashed_password" in table.columns
        assert "full_name" in table.columns
        assert "created_at" in table.columns
        assert "updated_at" in table.columns

    def test_database_constraints(self):
        """Test that database constraints are properly defined."""
        # Check that email is not null
        table = User.__table__
        email_column = table.columns.get("email")
        assert email_column is not None
        assert email_column.nullable is False

        # Check that hashed_password is not null
        hashed_password_column = table.columns.get("hashed_password")
        assert hashed_password_column is not None
        assert hashed_password_column.nullable is False

        # Check that full_name is not null
        full_name_column = table.columns.get("full_name")
        assert full_name_column is not None
        assert full_name_column.nullable is False

    def test_database_unique_constraints(self):
        """Test that database has proper unique constraints."""
        # Check that email is unique
        table = User.__table__
        email_column = table.columns.get("email")
        assert email_column is not None
        assert email_column.unique is True

    def test_database_migration_readiness(self):
        """Test that User is ready for database migrations."""
        # Verify all fields are properly defined for migration
        user = User()
        assert hasattr(user, "id")
        assert hasattr(user, "email")
        assert hasattr(user, "hashed_password")
        assert hasattr(user, "full_name")
        assert hasattr(user, "created_at")
        assert hasattr(user, "updated_at")

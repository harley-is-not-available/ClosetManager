"""
Tests for the base model configuration and database setup.
"""

from unittest.mock import Mock

import pytest

from backend.models.base import Base, BaseModel


class TestBaseModel:
    """Tests for the base model functionality."""

    def test_base_model_inheritance(self):
        """Test that BaseModel properly inherits from Base."""

        # Create a simple model that inherits from BaseModel
        class TestModel(BaseModel):
            __tablename__ = "test"

        # Verify it inherits from Base
        assert hasattr(TestModel, "__table__")
        assert TestModel.__table__.name == "test"

    def test_base_model_has_common_fields(self):
        """Test that BaseModel has the expected common fields."""
        # Create an instance of BaseModel
        model_instance = BaseModel()

        # Check that common fields exist
        assert hasattr(model_instance, "created_at")
        assert hasattr(model_instance, "updated_at")

    def test_base_model_to_dict_method(self):
        """Test the to_dict method of BaseModel."""

        # Create a simple test instance
        class TestModel(BaseModel):
            __tablename__ = "test"
            id: int = 1
            name: str = "test"

        model_instance = TestModel()
        model_instance.id = 1
        model_instance.name = "test"

        # Test to_dict method
        result = model_instance.to_dict()
        assert isinstance(result, dict)
        assert result.get("id") == 1
        assert result.get("name") == "test"
        assert "created_at" in result
        assert "updated_at" in result

    def test_base_model_repr_method(self):
        """Test the __repr__ method of BaseModel."""

        class TestModel(BaseModel):
            __tablename__ = "test"
            id: int = 1

        model_instance = TestModel()
        model_instance.id = 1

        # Test repr method
        result = repr(model_instance)
        assert result.startswith("<TestModel(id=1)>")
        assert "TestModel" in result


class TestDatabaseConfiguration:
    """Tests for the database configuration and setup."""

    def test_settings_loaded_correctly(self):
        """Test that database settings are loaded correctly."""
        # Check that settings have the expected attributes
        from backend.config.settings import settings

        assert hasattr(settings, "postgresql_url")
        assert hasattr(settings, "mongodb_url")
        assert hasattr(settings, "postgresql_pool_size")
        assert hasattr(settings, "postgresql_max_overflow")

    def test_postgresql_engine_creation(self):
        """Test that PostgreSQL engine is created correctly."""
        # Import engine from config to ensure it exists
        from backend.config.database import engine

        assert engine is not None

    def test_postgresql_session_factory(self):
        """Test that PostgreSQL session factory is created correctly."""
        # Import SessionLocal from config to ensure it exists
        from backend.config.database import SessionLocal

        assert SessionLocal is not None

    def test_mongodb_client_creation(self):
        """Test that MongoDB client is created correctly."""
        # Import mongo_client from config to ensure it exists
        from backend.config.database import mongo_client

        assert mongo_client is not None

    def test_mongodb_database(self):
        """Test that MongoDB database connection is established."""
        # Import db from config to ensure it exists
        from backend.config.database import db

        assert db is not None

    def test_get_db_generator(self):
        """Test that get_db is a generator function."""
        # Import get_db from config to ensure it exists
        import inspect

        from backend.config.database import get_db

        assert inspect.isgeneratorfunction(get_db)

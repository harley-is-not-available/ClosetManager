"""
Tests for the UploadService implementation.
These tests follow the same patterns as the item service tests.
"""

from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from backend.models.clothing_item import ClothingItem as ClothingItemModel
from backend.schemas.clothing_item import ClothingItemCreate
from backend.services.upload_service import UploadService


class TestUploadServiceFileHandling:
    """Tests for file upload functionality."""

    def test_upload_image_success(self, db_session: Session, tmp_path: Path):
        """Test successful image upload."""
        # Create a temporary file
        test_file = tmp_path / "test_image.jpg"
        test_file.write_text("fake image content")

        upload_service = UploadService(db_session, str(tmp_path))

        # Create a clothing item first
        item_data = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description="A test t-shirt",
            category="Tops",
            size="M",
            color="Blue",
            price=29.99,
            purchase_date=datetime.now(),
            image_path=None,
        )

        db_item = ClothingItemModel(**item_data.model_dump())
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)

        # Upload the image
        result = upload_service.upload_image(str(test_file), db_item.id, 1)

        assert result is not None
        assert result.image_path is not None
        assert result.image_path.startswith(str(tmp_path))

        # Check that file exists
        file_path = Path(result.image_path)
        assert file_path.exists()

    def test_upload_image_nonexistent_item(self, db_session: Session, tmp_path: Path):
        """Test uploading image to non-existent item."""
        # Create a temporary file
        test_file = tmp_path / "test_image.jpg"
        test_file.write_text("fake image content")

        upload_service = UploadService(db_session, str(tmp_path))

        # Try to upload to a non-existent item
        result = upload_service.upload_image(str(test_file), 99999, 1)

        assert result is None

    def test_upload_image_wrong_user(self, db_session: Session, tmp_path: Path):
        """Test uploading image to item owned by different user."""
        # Create a temporary file
        test_file = tmp_path / "test_image.jpg"
        test_file.write_text("fake image content")

        upload_service = UploadService(db_session, str(tmp_path))

        # Create a clothing item with user_id=1
        item_data = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description="A test t-shirt",
            category="Tops",
            size="M",
            color="Blue",
            price=29.99,
            purchase_date=datetime.now(),
            image_path=None,
        )

        db_item = ClothingItemModel(**item_data.model_dump())
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)

        # Try to upload with user_id=2 (different user)
        result = upload_service.upload_image(str(test_file), db_item.id, 2)

        assert result is None

    def test_upload_image_file_not_found(self, db_session: Session, tmp_path: Path):
        """Test uploading non-existent file."""
        upload_service = UploadService(db_session, str(tmp_path))

        # Create a clothing item
        item_data = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description="A test t-shirt",
            category="Tops",
            size="M",
            color="Blue",
            price=29.99,
            purchase_date=datetime.now(),
            image_path=None,
        )

        db_item = ClothingItemModel(**item_data.model_dump())
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)

        # Try to upload a non-existent file
        result = upload_service.upload_image("/non/existent/file.jpg", db_item.id, 1)

        assert result is None

    def test_upload_image_with_special_characters(
        self, db_session: Session, tmp_path: Path
    ):
        """Test uploading image with special characters in filename."""
        # Create a temporary file with special characters
        test_file = tmp_path / "test_image_äöü.jpg"
        test_file.write_text("fake image content")

        upload_service = UploadService(db_session, str(tmp_path))

        # Create a clothing item first
        item_data = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description="A test t-shirt",
            category="Tops",
            size="M",
            color="Blue",
            price=29.99,
            purchase_date=datetime.now(),
            image_path=None,
        )

        db_item = ClothingItemModel(**item_data.model_dump())
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)

        # Upload the image
        result = upload_service.upload_image(str(test_file), db_item.id, 1)

        assert result is not None
        assert result.image_path is not None
        assert "äöü" in result.image_path

    def test_unique_filename_generation(self, db_session: Session, tmp_path: Path):
        """Test that unique filenames are generated using UUID."""
        # Create a temporary file
        test_file = tmp_path / "test_image.jpg"
        test_file.write_text("fake image content")

        upload_service = UploadService(db_session, str(tmp_path))

        # Create a clothing item first
        item_data = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description="A test t-shirt",
            category="Tops",
            size="M",
            color="Blue",
            price=29.99,
            purchase_date=datetime.now(),
            image_path=None,
        )

        db_item = ClothingItemModel(**item_data.model_dump())
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)

        # Upload the image
        result = upload_service.upload_image(str(test_file), db_item.id, 1)

        assert result is not None
        assert result.image_path is not None

        # Verify that the filename contains a UUID (not just timestamp)
        # UUID should be 32 characters long (hex) plus underscore
        filename = Path(result.image_path).name
        assert "_" in filename
        # Should have UUID at the start
        parts = filename.split("_")
        assert len(parts) >= 2
        # First part should be 32-character hex UUID
        assert len(parts[0]) == 32
        assert all(c in "0123456789abcdef" for c in parts[0])


class TestUploadServiceImageDeletion:
    """Tests for image deletion functionality."""

    def test_delete_image_success(self, db_session: Session, tmp_path: Path):
        """Test successful image deletion."""
        # Create a temporary file
        test_file = tmp_path / "test_image.jpg"
        test_file.write_text("fake image content")

        upload_service = UploadService(db_session, str(tmp_path))

        # Create a clothing item with an image
        item_data = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description="A test t-shirt",
            category="Tops",
            size="M",
            color="Blue",
            price=29.99,
            purchase_date=datetime.now(),
            image_path=None,
        )

        db_item = ClothingItemModel(**item_data.model_dump())
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)

        # Upload an image first
        upload_result = upload_service.upload_image(str(test_file), db_item.id, 1)
        assert upload_result is not None
        assert upload_result.image_path is not None

        # Delete the image
        delete_result = upload_service.delete_image(db_item.id, 1)

        assert delete_result is True

        # Verify the image path is cleared from the database
        db_session.refresh(db_item)
        assert db_item.image_path is None

    def test_delete_image_nonexistent_item(self, db_session: Session, tmp_path: Path):
        """Test deleting image from non-existent item."""
        upload_service = UploadService(db_session, str(tmp_path))

        # Try to delete image from a non-existent item
        result = upload_service.delete_image(99999, 1)

        assert result is False

    def test_delete_image_nonexistent_image(self, db_session: Session, tmp_path: Path):
        """Test deleting image when item has no image."""
        upload_service = UploadService(db_session, str(tmp_path))

        # Create a clothing item without an image
        item_data = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description="A test t-shirt",
            category="Tops",
            size="M",
            color="Blue",
            price=29.99,
            purchase_date=datetime.now(),
            image_path=None,
        )

        db_item = ClothingItemModel(**item_data.model_dump())
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)

        # Try to delete image when there is none
        result = upload_service.delete_image(db_item.id, 1)

        assert result is False

    def test_delete_image_wrong_user(self, db_session: Session, tmp_path: Path):
        """Test deleting image from item owned by different user."""
        # Create a temporary file
        test_file = tmp_path / "test_image.jpg"
        test_file.write_text("fake image content")

        upload_service = UploadService(db_session, str(tmp_path))

        # Create a clothing item with user_id=1
        item_data = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description="A test t-shirt",
            category="Tops",
            size="M",
            color="Blue",
            price=29.99,
            purchase_date=datetime.now(),
            image_path=None,
        )

        db_item = ClothingItemModel(**item_data.model_dump())
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)

        # Upload an image first
        upload_service.upload_image(str(test_file), db_item.id, 1)

        # Try to delete with user_id=2 (different user)
        result = upload_service.delete_image(db_item.id, 2)

        assert result is False

    def test_upload_image_replaces_existing_file(
        self, db_session: Session, tmp_path: Path
    ):
        """Test that uploading a new image replaces the existing one and cleans up."""
        # Create two temporary files
        test_file1 = tmp_path / "original.jpg"
        test_file1.write_text("original content")

        test_file2 = tmp_path / "updated.jpg"
        test_file2.write_text("updated content")

        upload_service = UploadService(db_session, str(tmp_path))

        # Create a clothing item
        item_data = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description="A test t-shirt",
            category="Tops",
            size="M",
            color="Blue",
            price=29.99,
            purchase_date=datetime.now(),
            image_path=None,
        )

        db_item = ClothingItemModel(**item_data.model_dump())
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)

        # Upload first image
        result1 = upload_service.upload_image(str(test_file1), db_item.id, 1)
        assert result1 is not None
        assert result1.image_path is not None
        first_file_path = Path(result1.image_path)
        assert first_file_path.exists()

        # Upload second image (should replace and delete old)
        result2 = upload_service.upload_image(str(test_file2), db_item.id, 1)
        assert result2 is not None

        # Old file should no longer exist
        assert not first_file_path.exists()

        # New file should exist
        assert result2.image_path is not None
        new_file_path = Path(result2.image_path)
        assert new_file_path.exists()


class TestUploadServiceDatabaseConnection:
    """Tests for database connection handling."""

    def test_service_initialization_with_session(
        self, db_session: Session, tmp_path: Path
    ):
        """Test that service initializes correctly with a database session."""
        upload_service = UploadService(db_session, str(tmp_path))

        assert upload_service.db_session == db_session
        assert upload_service.upload_dir == Path(tmp_path)

    def test_service_methods_exist_and_are_callable(
        self, db_session: Session, tmp_path: Path
    ):
        """Test that all required service methods exist and are callable."""
        upload_service = UploadService(db_session, str(tmp_path))

        assert callable(upload_service.upload_image)
        assert callable(upload_service.delete_image)
        assert callable(upload_service.get_upload_directory)
        assert callable(upload_service.ensure_upload_directory_exists)


class TestUploadServiceErrorConditions:
    """Tests for error conditions and edge cases."""

    def test_upload_image_empty_file_path(self, db_session: Session, tmp_path: Path):
        """Test uploading with empty file path."""
        upload_service = UploadService(db_session, str(tmp_path))

        # Create a clothing item first
        item_data = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description="A test t-shirt",
            category="Tops",
            size="M",
            color="Blue",
            price=29.99,
            purchase_date=datetime.now(),
            image_path=None,
        )

        db_item = ClothingItemModel(**item_data.model_dump())
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)

        # Try to upload with empty path
        result = upload_service.upload_image("", db_item.id, 1)

        assert result is None

    def test_get_upload_directory(self, db_session: Session, tmp_path: Path):
        """Test getting upload directory."""
        upload_service = UploadService(db_session, str(tmp_path))

        result = upload_service.get_upload_directory()

        assert result == str(tmp_path)

    def test_ensure_upload_directory_exists(self, db_session: Session, tmp_path: Path):
        """Test ensuring upload directory exists."""
        upload_service = UploadService(db_session, str(tmp_path))

        result = upload_service.ensure_upload_directory_exists()

        assert result is True
        assert tmp_path.exists()

    def test_upload_image_with_multiple_files(
        self, db_session: Session, tmp_path: Path
    ):
        """Test uploading multiple files for the same item."""
        # Create two temporary files
        test_file1 = tmp_path / "test_image1.jpg"
        test_file1.write_text("fake image content 1")

        test_file2 = tmp_path / "test_image2.jpg"
        test_file2.write_text("fake image content 2")

        upload_service = UploadService(db_session, str(tmp_path))

        # Create a clothing item first
        item_data = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description="A test t-shirt",
            category="Tops",
            size="M",
            color="Blue",
            price=29.99,
            purchase_date=datetime.now(),
            image_path=None,
        )

        db_item = ClothingItemModel(**item_data.model_dump())
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)

        # Upload first image
        result1 = upload_service.upload_image(str(test_file1), db_item.id, 1)
        assert result1 is not None

        # Upload second image (should overwrite and clean up old file)
        result2 = upload_service.upload_image(str(test_file2), db_item.id, 1)
        assert result2 is not None

        # The second upload should have a different file path
        assert result1.image_path != result2.image_path

    def test_delete_image_file_not_found(self, db_session: Session, tmp_path: Path):
        """Test deleting image when file doesn't exist on disk."""
        upload_service = UploadService(db_session, str(tmp_path))

        # Create a clothing item without an image path
        item_data = ClothingItemCreate(
            name="Test T-Shirt",
            user_id=1,
            description="A test t-shirt",
            category="Tops",
            size="M",
            color="Blue",
            price=29.99,
            purchase_date=datetime.now(),
            image_path=None,
        )

        db_item = ClothingItemModel(**item_data.model_dump())
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)

        # Try to delete the image (no image exists)
        result = upload_service.delete_image(db_item.id, 1)

        # Should return False since there's no image to delete
        assert result is False

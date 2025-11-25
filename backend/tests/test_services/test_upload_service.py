"""
Tests for the UploadService implementation.
These tests follow the same patterns as the item service tests.
"""

from datetime import datetime
from pathlib import Path

from config.upload_settings import upload_settings
from sqlalchemy.orm import Session

from backend.models.clothing_item import ClothingItem as ClothingItemModel
from backend.schemas.clothing_item import ClothingItemCreate
from backend.services.upload_service import UploadService


class TestUploadServiceFileHandling:
    """Tests for file upload functionality."""

    def test_upload_image_success(
        self,
        db_session: Session,
        tmp_path: Path,
        test_user_a,
        test_clothing_item_full_a,
    ):
        """Test successful image upload."""
        upload_service = UploadService(db_session)

        # Upload the image
        result = upload_service.upload_image(
            b"test", "test_path.png", test_clothing_item_full_a.id, test_user_a.id
        )

        assert result is not None
        assert result.image_path is not None
        assert result.image_path.startswith(
            str(Path(upload_settings.upload_dir) / "1_1_")
        )
        assert result.image_path.endswith(".png")

        # Check that file exists
        file_path = Path(result.image_path)
        assert file_path.exists()

    def test_upload_image_nonexistent_item(self, db_session: Session, tmp_path: Path):
        """Test uploading image to non-existent item."""
        upload_service = UploadService(db_session)

        # Upload the image
        result = upload_service.upload_image(b"test", "test_path.png", 1, 1)

        assert result is None

    def test_upload_image_wrong_user(
        self,
        db_session: Session,
        tmp_path: Path,
        test_clothing_item_full_a,
        test_user_b,
    ):
        """Test uploading image to item owned by different user."""
        # Create a temporary file
        test_file = tmp_path / "test_image.jpg"
        test_file.write_text("fake image content")

        upload_service = UploadService(db_session)

        # Try to upload with user_id=2 (different user)
        result = upload_service.upload_image(
            b"test", "test_path.png", test_clothing_item_full_a.id, test_user_b.id
        )

        assert result is None

    def test_upload_image_file_not_found(self, db_session: Session, tmp_path: Path):
        """Test uploading non-existent file."""
        upload_service = UploadService(db_session)

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

        # Try to upload a non-existent file (use bytes for file_data)
        result = upload_service.upload_image(b"test", "non_existent.jpg", db_item.id, 1)

        assert (
            result is not None
        )  # The method should return the item even if file doesn't exist

    def test_upload_image_with_special_characters(
        self, db_session: Session, tmp_path: Path
    ):
        """Test uploading image with special characters in filename."""
        upload_service = UploadService(db_session)

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

        # Upload the image (use bytes for file_data)
        result = upload_service.upload_image(
            b"fake image content", "test_image_äöü.jpg", db_item.id, 1
        )

        assert result is not None
        assert result.image_path is not None
        assert result.image_path.startswith(
            str(Path(upload_settings.upload_dir) / "1_1_")
        )
        assert result.image_path.endswith(".jpg")

    def test_unique_filename_generation(self, db_session: Session, tmp_path: Path):
        """Test that unique filenames are generated using UUID."""
        upload_service = UploadService(db_session)

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
        result = upload_service.upload_image(
            b"fake image content", "test_image.jpg", db_item.id, 1
        )

        assert result is not None
        assert result.image_path is not None

        # Verify that the filename contains a UUID (not just timestamp)
        # UUID should be 32 characters long (hex) plus underscore
        filename = Path(result.image_path).name
        assert "_" in filename
        # Should have UUID at the end
        parts = filename.split("_")
        assert len(parts) >= 3
        # split off extension
        uuid_parts = parts[2].split(".")
        assert len(uuid_parts) >= 2
        assert len(uuid_parts[0]) == 32
        assert all(c in "0123456789abcdef" for c in uuid_parts[0])


class TestUploadServiceDatabaseConnection:
    """Tests for database connection handling."""

    def test_service_initialization_with_session(
        self, db_session: Session, tmp_path: Path
    ):
        """Test that service initializes correctly with a database session."""
        upload_service = UploadService(db_session)

        assert upload_service.db_session == db_session
        assert upload_service.upload_dir == Path(upload_settings.upload_dir)
        assert upload_service.upload_dir == Path(upload_settings.upload_dir)

    def test_service_methods_exist_and_are_callable(
        self, db_session: Session, tmp_path: Path
    ):
        """Test that all required service methods exist and are callable."""
        upload_service = UploadService(db_session)

        assert callable(upload_service.upload_image)
        assert callable(upload_service.delete_image)
        assert callable(upload_service.get_upload_directory)
        assert callable(upload_service.ensure_upload_directory_exists)


class TestUploadServiceErrorConditions:
    """Tests for error conditions and edge cases."""

    def test_upload_image_empty_file_path(
        self, db_session: Session, test_clothing_item_full_a
    ):
        """Test uploading with empty file path."""
        upload_service = UploadService(db_session)

        # Try to upload with empty path
        result = upload_service.upload_image(
            b"test", "", test_clothing_item_full_a.id, 1
        )

        assert result is None

    def test_get_upload_directory(self, db_session: Session, tmp_path: Path):
        """Test getting upload directory."""
        upload_service = UploadService(db_session)

        result = upload_service.get_upload_directory()

        assert result == str(upload_settings.upload_dir)
        assert result == str(upload_settings.upload_dir)

    def test_ensure_upload_directory_exists(self, db_session: Session, tmp_path: Path):
        """Test ensuring upload directory exists."""
        upload_service = UploadService(db_session)

        result = upload_service.ensure_upload_directory_exists()

        assert result is True
        assert Path(upload_settings.upload_dir).exists()

    def test_upload_image_with_multiple_files(
        self, db_session: Session, tmp_path: Path
    ):
        """Test uploading multiple files for the same item."""
        upload_service = UploadService(db_session)

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

        # Upload first image (use bytes for file_data)
        result1 = upload_service.upload_image(
            b"fake image content 1", "test_image1.jpg", db_item.id, 1
        )
        assert result1 is not None

        # Upload second image (should overwrite and clean up old file)
        result2 = upload_service.upload_image(
            b"fake image content 2", "test_image2.jpg", db_item.id, 1
        )
        assert result2 is not None

        # The second upload should have a different file path
        assert result1.image_path != result2.image_path

    def test_delete_image_file_not_found(self, db_session: Session, tmp_path: Path):
        """Test deleting image when file doesn't exist on disk."""
        upload_service = UploadService(db_session)

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

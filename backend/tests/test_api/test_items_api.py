"""
Test cases for the Items API endpoints.
These tests cover all CRUD operations for clothing items.
"""

import base64
import json
from datetime import datetime
from io import BytesIO
from unittest.mock import Mock

from backend.api.v1.items import get_item_service
from backend.schemas.clothing_item import ClothingItem, ClothingItemCreate
from backend.services.item_service import ItemService


def test_get_items_success(
    override_get_db,
    client,
    test_user_a,
    test_clothing_item_partial_a,
    test_clothing_item_full_a,
    override_item_service,
    mock_item_service_instance,
):
    """
    Test successful retrieval of all items for a user.
    """
    # Configure the mock to return the test items
    mock_item_service_instance.get_all_items.return_value = [
        test_clothing_item_partial_a,
        test_clothing_item_full_a,
    ]

    # Make the request
    response = client.get("/api/v1/items", params={"user_id": test_user_a.id})

    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Test T-Shirt"
    assert data[1]["name"] == "Test T-Shirt"
    assert data[0]["description"] == "A test t-shirt"
    assert data[0]["category"] == "Tops"
    assert data[1]["description"] == "A test t-shirt"
    assert data[1]["category"] == "Tops"
    assert data[0]["id"] == test_clothing_item_partial_a.id
    assert data[1]["id"] == test_clothing_item_full_a.id


def test_get_items_empty_list(
    override_get_db,
    client,
    test_user_a,
    override_item_service,
    mock_item_service_instance,
):
    """
    Test retrieval of items when user has no items.
    """
    # Configure the mock to return an empty list
    mock_item_service_instance.get_all_items.return_value = []

    # Make the request
    response = client.get("/api/v1/items", params={"user_id": test_user_a.id})

    # Verify the response
    assert response.status_code == 201
    assert response.json()["detail"] == "No items found for this user"


def test_get_item_success(
    override_get_db,
    client,
    test_user_a,
    test_clothing_item_partial_a,
    override_item_service,
    mock_item_service_instance,
):
    """
    Test successful retrieval of a specific item by ID.
    """
    # Configure the mock to return the test item
    mock_item_service_instance.get_item.return_value = test_clothing_item_partial_a

    # Make the request
    response = client.get(
        f"/api/v1/items/{test_clothing_item_partial_a.id}",
        params={"user_id": test_user_a.id},
    )

    # Verify the response
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test T-Shirt"
    assert data["user_id"] == test_user_a.id


def test_get_item_not_found(
    override_get_db,
    client,
    test_user_a,
    override_item_service,
    mock_item_service_instance,
):
    """
    Test retrieval of non-existent item.
    """
    # Configure the mock to return None (item not found)
    mock_item_service_instance.get_item.return_value = None

    # Make the request
    response = client.get("/api/v1/items/99999", params={"user_id": test_user_a.id})

    # Verify the response
    assert response.status_code == 404
    assert "Item not found or not owned by user" in response.json()["detail"]


def test_create_item_success(
    override_get_db,
    client,
    test_user_a,
    test_clothing_item_full_a,
    override_item_service,
    mock_item_service_instance,
):
    """
    Test successful creation of a new item by consolidating all form parts
    into the 'files' argument for clean multipart/form-data encoding.
    """
    # Configure the mock to return the created item
    mock_item_service_instance.create_item.return_value = test_clothing_item_full_a

    # Create a mock item data that matches what would be sent from a real client
    data = ClothingItemCreate(
        name="Test T-Shirt",
        user_id=test_user_a.id,
        description="A test t-shirt",
        category="Tops",
        # Ensure all required fields for your Pydantic model are included
        size=None,
        color=None,
        price=None,
        purchase_date=None,
        image_data=base64.b64encode(b"test").decode("utf-8"),
        image_name="test.jpg",
    )
    # Make the request using form data and files
    response = client.post(
        "/api/v1/items", params={"user_id": test_user_a.id}, json=data.model_dump()
    )

    # Verify the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "Test T-Shirt"
    assert response_data["user_id"] == test_user_a.id

    # Optional: Verify service call arguments (optional check for completeness)
    mock_item_service_instance.create_item.assert_called_once()

    assert response_data["image_data"] is not None


def test_update_item_success(
    override_get_db,
    client,
    test_user_a,
    test_clothing_item_full_a,
    override_item_service,
    mock_item_service_instance,
):
    """
    Test successful update of an existing item.
    """
    test_clothing_item_full_a.name = "Updated T-Shirt"

    # Configure the mock to return the updated item
    mock_item_service_instance.update_item.return_value = test_clothing_item_full_a

    # Create a mock item data that matches what would be sent from a real client
    data = ClothingItemCreate(
        name="Updated T-Shirt",
        user_id=test_user_a.id,
        description="An updated test t-shirt",
        category="Tops",
        # Ensure all required fields for your Pydantic model are included
        size=None,
        color=None,
        price=None,
        purchase_date=None,
        image_data=base64.b64encode(b"test").decode("utf-8"),
        image_name="test.jpg",
    )

    # Make the request using form data and files
    response = client.put(
        f"/api/v1/items/{test_clothing_item_full_a.id}",
        params={"user_id": test_user_a.id},
        json=data.model_dump(),
    )

    # Verify the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "Updated T-Shirt"
    assert response_data["user_id"] == test_user_a.id

    # Optional: Verify service call arguments (optional check for completeness)
    mock_item_service_instance.update_item.assert_called_once()

    assert response_data["image_data"] is not None


def test_update_item_not_found(
    override_get_db,
    client,
    test_user_a,
    override_item_service,
    mock_item_service_instance,
):
    """
    Test update of non-existent item.
    """
    # Configure the mock to return None (item not found)
    mock_item_service_instance.update_item.return_value = None

    # Create a mock item data that matches what would be sent from a real client
    data = ClothingItemCreate(
        name="Updated T-Shirt",
        user_id=test_user_a.id,
        description="An updated test t-shirt",
        category="Tops",
        # Ensure all required fields for your Pydantic model are included
        size=None,
        color=None,
        price=None,
        purchase_date=None,
        image_data=base64.b64encode(b"test").decode("utf-8"),
        image_name="test.jpg",
    )

    # Make the request with proper data structure
    response = client.put(
        "/api/v1/items/99999",
        params={"user_id": test_user_a.id},
        json=data.model_dump(),
    )

    # Verify the response
    assert response.status_code == 404
    assert "Item not found or not owned by user" in response.json()["detail"]


def test_delete_item_success(
    override_get_db,
    client,
    test_user_a,
    test_clothing_item_partial_a,
    override_item_service,
    mock_item_service_instance,
):
    """
    Test successful deletion of an item.
    """
    # Configure the mock to return True (successful deletion)
    mock_item_service_instance.delete_item.return_value = True

    # Make the request
    response = client.delete(
        f"/api/v1/items/{test_clothing_item_partial_a.id}",
        params={"user_id": test_user_a.id},
    )

    # Verify the response
    assert response.status_code == 204


def test_delete_item_not_found(
    override_get_db,
    client,
    test_user_a,
    override_item_service,
    mock_item_service_instance,
):
    """
    Test deletion of non-existent item.
    """
    # Configure the mock to return False (item not found)
    mock_item_service_instance.delete_item.return_value = False

    # Make the request
    response = client.delete("/api/v1/items/99999", params={"user_id": test_user_a.id})

    # Verify the response
    assert response.status_code == 404
    assert "Item not found or not owned by user" in response.json()["detail"]


def test_items_api_structure(override_get_db, client):
    """
    Test that items endpoints exist and are callable.
    """
    # Test GET /api/v1/items
    response = client.get("/api/v1/items")
    assert response.status_code in [400, 422]  # Bad request or validation error

    # Test GET /api/v1/items/{id}
    response = client.get("/api/v1/items/1")
    assert response.status_code in [400, 422]  # Bad request or validation error

    # Test POST /api/v1/items
    response = client.post("/api/v1/items")
    assert response.status_code in [400, 422]  # Bad request or validation error

    # Test PUT /api/v1/items/{id}
    response = client.put("/api/v1/items/1")
    assert response.status_code in [400, 422]  # Bad request or validation error

    # Test DELETE /api/v1/items/{id}
    response = client.delete("/api/v1/items/1")
    assert response.status_code in [400, 422]  # Bad request or validation error


def test_create_item_invalid_data(override_get_db, client, test_user_a):
    """
    Test creation of item with invalid data.
    """
    # Make the request with incomplete data
    response = client.post(
        "/api/v1/items",
        params={"user_id": test_user_a.id},
        json={
            "name": "",  # Invalid: empty name
        },
    )
    assert response.status_code == 422


def test_update_item_invalid_data(
    override_get_db, client, test_user_a, test_clothing_item_partial_a
):
    """
    Test update of item with invalid data.
    """
    # Make the request with invalid data
    response = client.put(
        f"/api/v1/items/{test_clothing_item_partial_a.id}",
        params={"user_id": test_user_a.id},
        json={
            "name": "",  # Invalid: empty name
        },
    )

    # Verify the response
    assert response.status_code == 422


def test_get_items_invalid_user_id(
    override_get_db,
    client,
    test_user_a,
    override_item_service,
    mock_item_service_instance,
):
    """
    Test retrieval of items with invalid user ID.
    """
    # Configure the mock to return an empty list for invalid user
    mock_item_service_instance.get_all_items.return_value = []

    # Make request with invalid user ID
    response = client.get("/api/v1/items", params={"user_id": -1})
    assert response.status_code == 201
    # TODO in the future in [400, 422]


def test_get_item_invalid_user_id(
    override_get_db,
    client,
    test_clothing_item_partial_a,
    override_item_service,
    mock_item_service_instance,
):
    """
    Test retrieval of specific item with invalid user ID.
    """
    # Configure the mock to return None for invalid user
    mock_item_service_instance.get_item.return_value = None

    response = client.get(
        f"/api/v1/items/{test_clothing_item_partial_a.id}", params={"user_id": -1}
    )
    # TODO 404 should not be returned, when properly handling validation.
    assert response.status_code in [400, 422, 404]

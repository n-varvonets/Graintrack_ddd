# tests/presentation/api/v1/test_categories.py
import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_category(async_client: AsyncClient):
    """Test the creation of a new category with a randomly generated UUID as its parent category ID."""
    category_data = {
        "name": "Electronics",
        "parent_category_id": str(uuid.uuid4())
    }
    response = await async_client.post("/api/v1/categories/", json=category_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == category_data["name"]
    assert data["parent_category_id"] == category_data["parent_category_id"]


@pytest.mark.asyncio
async def test_create_category_with_parent(async_client: AsyncClient):
    """Test the creation of a sub-category with a specific parent category, verifying both are correctly linked."""
    parent_category_data = {
        "name": "Electronics",
        "parent_category_id": None
    }
    parent_response = await async_client.post("/api/v1/categories/", json=parent_category_data)
    assert parent_response.status_code == 201
    parent_id = parent_response.json()["id"]

    # Now, create a sub-category
    sub_category_data = {
        "name": "Smartphones",
        "parent_category_id": parent_id
    }
    sub_response = await async_client.post("/api/v1/categories/", json=sub_category_data)
    assert sub_response.status_code == 201
    data = sub_response.json()
    assert data["name"] == sub_category_data["name"]
    assert data["parent_category_id"] == parent_id


@pytest.mark.asyncio
async def test_update_category(async_client: AsyncClient):
    """Test updating a category's name to ensure partial updates are handled correctly."""
    category_data = {
        "name": "Electronics",
        "parent_category_id": None
    }
    create_response = await async_client.post("/api/v1/categories/", json=category_data)
    assert create_response.status_code == 201
    category_id = create_response.json()["id"]

    # Update the category partially
    update_data = {
        "name": "Home Electronics"
    }
    update_response = await async_client.patch(f"/api/v1/categories/{category_id}/", json=update_data)
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == update_data["name"]
    assert data["parent_category_id"] is None


@pytest.mark.asyncio
async def test_delete_category(async_client: AsyncClient):
    """Test the deletion of a category and ensuring it cannot be retrieved after deletion."""
    category_data = {
        "name": "Electronics",
        "parent_category_id": None
    }
    create_response = await async_client.post("/api/v1/categories/", json=category_data)
    assert create_response.status_code == 201
    category_id = create_response.json()["id"]

    # Delete the category
    delete_response = await async_client.delete(f"/api/v1/categories/{category_id}/")
    assert delete_response.status_code == 204

    # Try to retrieve the deleted category
    get_response = await async_client.get(f"/api/v1/categories/{category_id}/")
    assert get_response.status_code == 404

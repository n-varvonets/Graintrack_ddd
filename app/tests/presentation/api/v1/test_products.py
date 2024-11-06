# app/tests/presentation/api/v1/test_products.py

import pytest
import uuid


@pytest.mark.asyncio
async def test_create_product(async_client):
    """
    Tests the API endpoint for creating a new product, ensuring that the product is
    successfully created and that the response contains the correct product details.
    """
    product_data = {
        "name": "Test Product",
        "category_id": str(uuid.uuid4()),
        "price": 100.0,
        "stock": 10
    }

    response = await async_client.post("/api/v1/products/", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["price"] == product_data["price"]
    assert data["stock"] == product_data["stock"]


@pytest.mark.asyncio
async def test_get_products(async_client):
    """
    Verifies that the API endpoint for retrieving a list of products returns a
    successful response with a list of products.
    """
    # Assumes that a product has already been created in a previous test
    response = await async_client.get("/api/v1/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_product_by_id(async_client):
    """
    Ensures that the API endpoint for retrieving a specific product by its ID
    returns the correct product details.
    """
    product_data = {
        "name": "Test Product",
        "category_id": str(uuid.uuid4()),
        "price": 100.0,
        "stock": 10
    }
    create_response = await async_client.post("/api/v1/products/", json=product_data)
    product_id = create_response.json()["id"]

    # Retrieve the product by ID
    response = await async_client.get(f"/api/v1/products/{product_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id


@pytest.mark.asyncio
async def test_update_product(async_client):
    """
    Confirms that the API endpoint for updating a product successfully updates
    the product's details and returns the updated information.
    """
    product_data = {
        "name": "Old Product",
        "category_id": str(uuid.uuid4()),
        "price": 100.0,
        "stock": 10
    }
    create_response = await async_client.post("/api/v1/products/", json=product_data)
    product_id = create_response.json()["id"]

    # Update the product
    update_data = {
        "name": "Updated Product",
        "price": 150.0
    }
    response = await async_client.put(f"/api/v1/products/{product_id}/", json=update_data)
    if response.status_code != 200:
        print(response.json())  # Print validation errors
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["price"] == update_data["price"]


@pytest.mark.asyncio
async def test_delete_product(async_client):
    """
    Validates that the API endpoint for deleting a product successfully removes
    the product and that subsequent retrieval attempts return a 404 Not Found status.
    """
    product_data = {
        "name": "Product to Delete",
        "category_id": str(uuid.uuid4()),
        "price": 100.0,
        "stock": 10
    }
    create_response = await async_client.post("/api/v1/products/", json=product_data)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    response = await async_client.delete(f"/api/v1/products/{product_id}/")
    assert response.status_code == 204

    response = await async_client.get(f"/api/v1/products/{product_id}/")
    assert response.status_code == 404

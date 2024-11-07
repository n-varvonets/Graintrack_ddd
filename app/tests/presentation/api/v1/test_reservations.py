# app/tests/presentation/api/v1/test_reservations.py

import pytest
import uuid


@pytest.mark.asyncio
async def test_create_reservation(async_client):
    reservation_data = {
        "product_id": str(uuid.uuid4()),
        "quantity": 2
    }
    response = await async_client.post("/api/v1/reservations/", json=reservation_data)
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == reservation_data["product_id"]
    assert data["quantity"] == reservation_data["quantity"]


@pytest.mark.asyncio
async def test_cancel_reservation(async_client):
    # First, create a reservation to cancel
    reservation_data = {
        "product_id": str(uuid.uuid4()),
        "quantity": 2
    }
    create_response = await async_client.post("/api/v1/reservations/", json=reservation_data)
    reservation_id = create_response.json()["id"]

    # Now, cancel the reservation
    cancel_response = await async_client.delete(f"/api/v1/reservations/{reservation_id}/")
    assert cancel_response.status_code == 204

    # Verify cancellation by attempting to cancel again or fetching the reservation status
    # This part depends on your implementation

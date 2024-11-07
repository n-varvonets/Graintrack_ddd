# app/tests/presentation/api/v1/test_sales.py

import pytest
from datetime import datetime, timedelta
import uuid


@pytest.mark.asyncio
async def test_register_sale(async_client):
    sale_data = {
        "product_id": str(uuid.uuid4()),
        "quantity": 3
    }
    response = await async_client.post("/api/v1/sales/", json=sale_data)
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == sale_data["product_id"]
    assert data["quantity"] == sale_data["quantity"]


@pytest.mark.asyncio
async def test_get_sales(async_client):
    # Assume some sales are already recorded
    start_date = (datetime.now() - timedelta(days=1)).isoformat()
    end_date = (datetime.now() + timedelta(days=1)).isoformat()
    response = await async_client.get("/api/v1/sales/", params={
        "start_date": start_date,
        "end_date": end_date
    })
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

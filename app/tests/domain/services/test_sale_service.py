# tests/domain/services/test_sale_service.py

import pytest
from domain.services.sale_service import SaleService
from domain.entities.sale import Sale
from domain.exceptions.sale_exceptions import SaleNotFoundException
from datetime import datetime, timedelta
import uuid


@pytest.mark.asyncio
async def test_record_sale(sale_service):
    """
    Checks that a sale can be successfully recorded with the specified product ID
    and quantity.
    """
    sale_data = {
        "product_id": str(uuid.uuid4()),
        "quantity": 3
    }
    sale = await sale_service.record_sale(sale_data)
    assert sale.product_id == sale_data["product_id"]
    assert sale.quantity == 3


@pytest.mark.asyncio
async def test_get_sales_between_dates(sale_service):
    """
    Ensures that retrieving sales within a specified date range returns all relevant
    sales records.
    """
    product_id = str(uuid.uuid4())

    sale_data_1 = {
        "product_id": product_id,
        "quantity": 2
    }
    sale_data_2 = {
        "product_id": product_id,
        "quantity": 3
    }

    sale1 = await sale_service.record_sale(sale_data_1)
    sale2 = await sale_service.record_sale(sale_data_2)
    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now() + timedelta(days=1)
    sales = await sale_service.get_sales_report(start_date, end_date)
    assert len(sales) >= 2


@pytest.mark.asyncio
async def test_get_nonexistent_sale(sale_service):
    """
    Validates that attempting to retrieve a sale that does not exist results in
    a SaleNotFoundException.
    """
    non_existent_sale_id = str(uuid.uuid4())
    with pytest.raises(SaleNotFoundException):
        await sale_service.get_by_id(non_existent_sale_id)

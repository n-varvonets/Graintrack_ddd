# tests/domain/services/test_sale_service.py

import pytest
from app.domain.services.sale_service import SaleService
from app.domain.entities.sale import Sale
from app.domain.exceptions.sale_exceptions import SaleNotFoundException
from datetime import datetime, timedelta
import uuid


def test_record_sale(sale_service):
    product_id = str(uuid.uuid4())
    sale = sale_service.record_sale(product_id, 3)
    assert sale.product_id == product_id
    assert sale.quantity == 3


def test_get_sales_between_dates(sale_service):
    product_id = str(uuid.uuid4())
    sale1 = sale_service.record_sale(product_id, 2)
    sale2 = sale_service.record_sale(product_id, 3)
    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now() + timedelta(days=1)
    sales = sale_service.get_sales_report(start_date, end_date)
    assert len(sales) >= 2


def test_get_nonexistent_sale(sale_service):
    non_existent_sale_id = str(uuid.uuid4())
    with pytest.raises(SaleNotFoundException):
        sale_service.get_by_id(non_existent_sale_id)

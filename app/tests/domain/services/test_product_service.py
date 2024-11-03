# tests/domain/services/test_product_service.py

import pytest
from app.domain.services.product_service import ProductService
from app.domain.entities.product import Product
from app.domain.values.price import Price
from app.domain.values.quantity import Quantity
from app.domain.values.discount import Discount
from app.domain.exceptions.product_exceptions import ProductNotFoundException, InvalidDiscountException, InsufficientStockException
import uuid

def test_create_product(product_service):
    product = Product(
        name="Test Product",
        category_id=str(uuid.uuid4()),
        price=Price(100.0),
        stock=Quantity(10)
    )
    created_product = product_service.create_product(product)
    assert created_product == product

def test_get_available_products(product_service):
    category_id = str(uuid.uuid4())
    product1 = Product(
        name="Product 1",
        category_id=category_id,
        price=Price(50.0),
        stock=Quantity(5)
    )
    product2 = Product(
        name="Product 2",
        category_id=category_id,
        price=Price(75.0),
        stock=Quantity(1)
    )
    product_service.create_product(product1)
    product_service.create_product(product2)
    available_products = product_service.get_available_products(category_id=category_id)
    assert len(available_products) == 2
    assert available_products[0] == product1
    assert product2 in available_products


def test_apply_discount(product_service):
    product = Product(
        name="Discounted Product",
        category_id=str(uuid.uuid4()),
        price=Price(200.0),
        stock=Quantity(5)
    )
    product_service.create_product(product)
    updated_product = product_service.start_promotion(product.oid, 10.0)  # Скидка 10%
    assert updated_product.discount.value == 10.0
    assert updated_product.get_price_after_discount() == 180.0

def test_apply_invalid_discount(product_service):
    product = Product(
        name="Invalid Discount Product",
        category_id=str(uuid.uuid4()),
        price=Price(100.0),
        stock=Quantity(5)
    )
    product_service.create_product(product)
    with pytest.raises(InvalidDiscountException):
        product_service.start_promotion(product.oid, 150.0)  # Неверная скидка

def test_update_price_nonexistent_product(product_service):
    non_existent_product_id = str(uuid.uuid4())
    with pytest.raises(ProductNotFoundException):
        product_service.update_price(non_existent_product_id, Price(150.0))

def test_reserve_product_insufficient_stock(product_service):
    product = Product(
        name="Limited Stock Product",
        category_id=str(uuid.uuid4()),
        price=Price(50.0),
        stock=Quantity(2)
    )
    product_service.create_product(product)
    with pytest.raises(InsufficientStockException):
        product_service.reserve_product(product.oid, 5)

def test_sell_product_insufficient_stock(product_service):
    product = Product(
        name="Limited Stock Product",
        category_id=str(uuid.uuid4()),
        price=Price(50.0),
        stock=Quantity(2)
    )
    product_service.create_product(product)
    with pytest.raises(InsufficientStockException):
        product_service.sell_product(product.oid, 5)

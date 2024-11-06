# tests/domain/services/test_product_service.py

import pytest
from domain.entities.product import Product
from domain.values.price import Price
from domain.values.quantity import Quantity
from domain.exceptions.product_exceptions import ProductNotFoundException, InvalidDiscountException, InsufficientStockException
import uuid

from infrastructure.converters.product_converters import convert_product_to_dto


@pytest.mark.asyncio
async def test_create_product(product_service):
    """
    Verifies that a new product can be successfully created and that the created product
    matches the expected DTO representation.
    """
    product = Product(
        name="Test Product",
        category_id=str(uuid.uuid4()),
        price=Price(100.0),
        stock=Quantity(10)
    )
    created_product = await product_service.create_product(product)
    assert created_product == convert_product_to_dto(product)


@pytest.mark.asyncio
async def test_get_available_products(product_service):
    """
    Ensures that retrieving available products filtered by a specific category returns
    all products with a stock greater than zero within that category.
    """
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
    await product_service.create_product(product1)
    await product_service.create_product(product2)
    available_products = await product_service.get_available_products(category_id=category_id)
    assert len(available_products) == 2
    assert available_products[0] == product1
    assert product2 in available_products


@pytest.mark.asyncio
async def test_apply_discount(product_service):
    """
    Checks that applying a valid discount percentage to a product correctly updates
    the product's discount and calculates the price after discount accurately.
    """
    product = Product(
        name="Discounted Product",
        category_id=str(uuid.uuid4()),
        price=Price(200.0),
        stock=Quantity(5)
    )
    await product_service.create_product(product)
    updated_product = await product_service.start_promotion(product_id=product.oid, discount_percentage=10.0)
    assert updated_product.discount == 10.0
    assert updated_product.price_after_discount == 180.0


@pytest.mark.asyncio
async def test_apply_invalid_discount(product_service):
    """
    Confirms that applying an invalid discount percentage (e.g., exceeding 100%) to a
    product raises an InvalidDiscountException.
    """
    product = Product(
        name="Invalid Discount Product",
        category_id=str(uuid.uuid4()),
        price=Price(100.0),
        stock=Quantity(5)
    )
    await product_service.create_product(product)
    with pytest.raises(InvalidDiscountException):
        await product_service.start_promotion(
            product_id=product.oid,
            discount_percentage=150.0
        )


@pytest.mark.asyncio
async def test_update_price_nonexistent_product(product_service):
    """
    Validates that attempting to update the price of a non-existent product results in
    a ProductNotFoundException.
    """
    non_existent_product_id = str(uuid.uuid4())
    with pytest.raises(ProductNotFoundException):
        await product_service.update_price(
            non_existent_product_id,
            Price(150.0)
        )


@pytest.mark.asyncio
async def test_reserve_product_insufficient_stock(product_service):
    """
    Ensures that attempting to reserve a quantity of a product exceeding its available
    stock raises an InsufficientStockException.
    """
    product = Product(
        name="Limited Stock Product",
        category_id=str(uuid.uuid4()),
        price=Price(50.0),
        stock=Quantity(2)
    )
    await product_service.create_product(product)
    with pytest.raises(InsufficientStockException):
        await product_service.reserve_product(product_id=product.oid, quantity=5)


@pytest.mark.asyncio
async def test_sell_product_insufficient_stock(product_service):
    """
    Verifies that trying to sell a quantity of a product that exceeds its available
    stock triggers an InsufficientStockException.
    """
    product = Product(
        name="Limited Stock Product",
        category_id=str(uuid.uuid4()),
        price=Price(50.0),
        stock=Quantity(2)
    )
    await product_service.create_product(product)
    with pytest.raises(InsufficientStockException):
        await product_service.sell_product(product_id=product.oid, quantity=5)

# app/infrastructure/converters/product_converters.py
from typing import List
from domain.entities.product import Product
from domain.values.discount import Discount
from domain.values.price import Price
from domain.values.quantity import Quantity
from presentation.schemas.product_schema import ProductResponse, ProductCreateRequest


def convert_product_to_dto(product: Product) -> ProductResponse:
    """Converts a Product domain entity to a ProductResponse DTO."""
    discount_value = (
        getattr(product.discount, 'value', product.discount)
        if product.discount is not None else 0.0
    )

    return ProductResponse(
        id=str(product.oid),
        name=product.name,
        category_id=product.category_id,
        price=getattr(product, 'price_value', getattr(product, 'price', None)),
        stock=getattr(product, 'stock_value', getattr(product, 'stock', None)),
        discount=getattr(product, 'discount_value', getattr(product, 'discount', None)),
        description=getattr(product, 'description', ""),
        created_at=product.created_at,
        price_after_discount=(
            product.get_price_after_discount() if discount_value > 0 else getattr(product, 'price_value',
                                                                                  getattr(product, 'price', None))
        )
    )

def convert_dto_to_product(product_data: ProductCreateRequest) -> Product:
    """Converts a ProductResponse DTO back to a Product domain entity."""

    def get_numeric_value(value):
        """Рекурсивно извлекает числовое значение из объектов Price, Quantity или Discount."""
        while hasattr(value, "value"):
            value = value.value
        return value

    # Извлекаем числовые значения из price, stock и discount
    price_value = get_numeric_value(product_data.price)
    stock_value = get_numeric_value(product_data.stock)
    discount_value = get_numeric_value(getattr(product_data, 'discount', 0.0))

    return Product(
        name=product_data.name,
        category_id=str(product_data.category_id),
        price=Price(value=price_value),  # Передаем числовое значение
        stock=Quantity(value=stock_value),  # Передаем числовое значение
        discount=Discount(value=discount_value)  # Передаем числовое значение
    )

def convert_products_to_responses(products: List[Product]) -> List[ProductResponse]:
    """Преобразует список сущностей Product в список Pydantic-схем ProductResponse."""
    return [convert_product_to_dto(product) for product in products]

# app/infrastructure/repositories/in_memory/in_memory_product_repository.py
import uuid
from typing import List, Optional
from domain.entities.product import Product
from application.interfaces.product_repository_interface import ProductRepositoryInterface
from domain.exceptions.product_exceptions import ProductNotFoundException
from domain.values.price import Price
from domain.values.quantity import Quantity
from infrastructure.converters.product_converters import convert_dto_to_product, convert_product_to_dto, \
    convert_products_to_responses


class InMemoryProductRepository(ProductRepositoryInterface):
    """
    In-memory implementation of the ProductRepositoryInterface for testing purposes.
    """

    def __init__(self):
        self.products = {}

    async def add(self, product: Product) -> Product:
        self.products[product.oid] = product
        return product

    async def get_by_id(self, product_id: str) -> Optional[Product]:
        product = self.products.get(product_id)
        if not product:
            raise ProductNotFoundException(product_id=product_id)
        return product


    async def update(self, product: Product) -> Product:
        product_id = str(product.oid) if isinstance(product.oid, uuid.UUID) else product.oid

        if product_id not in self.products:
            raise ProductNotFoundException(product_id)

        self.products[product_id] = product
        return product

    async def delete(self, product_id: str) -> None:
        if product_id not in self.products:
            raise ProductNotFoundException(product_id)
        del self.products[product_id]

    async def get_all(self) -> List[Product]:
        return list(self.products.values())

    async def get_by_category(self, category_id: str) -> List[Product]:
        return [product for product in self.products.values() if product.category_id == category_id]

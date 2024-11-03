# app/infrastructure/repositories/in_memory/in_memory_product_repository.py

from typing import List, Optional
from app.domain.entities.product import Product
from app.application.interfaces.product_repository_interface import ProductRepositoryInterface
from app.domain.exceptions.product_exceptions import ProductNotFoundException


class InMemoryProductRepository(ProductRepositoryInterface):
    """
    In-memory implementation of the ProductRepositoryInterface for testing purposes.
    """

    def __init__(self):
        self.products = {}

    def add(self, product: Product) -> Product:
        self.products[product.oid] = product
        return product

    def get_by_id(self, product_id: str) -> Optional[Product]:
        product = self.products.get(product_id)
        if not product:
            raise ProductNotFoundException(product_id=product_id)
        return product

    def update(self, product: Product) -> Product:
        if product.oid not in self.products:
            raise ProductNotFoundException(product_id=product.oid)
        self.products[product.oid] = product
        return product

    def delete(self, product_id: str) -> None:
        if product_id not in self.products:
            raise ProductNotFoundException(product_id=product_id)
        del self.products[product_id]

    def get_all(self) -> List[Product]:
        return list(self.products.values())

    def get_by_category(self, category_id: str) -> List[Product]:
        return [product for product in self.products.values() if product.category_id == category_id]

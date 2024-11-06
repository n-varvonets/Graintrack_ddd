# app/tests/test_container.py
from domain.services.product_service import ProductService


def test_container_resolution(test_container):
    product_service = test_container.resolve(ProductService)
    assert product_service is not None
    assert isinstance(product_service, ProductService)

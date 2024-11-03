# app/presentation/api/v1/dependencies.py

from app.containers import container
from app.domain.services.product_service import ProductService

def get_product_service() -> ProductService:
    return container.resolve(ProductService)

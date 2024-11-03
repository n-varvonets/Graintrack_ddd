# app/containers.py

import punq
from app.domain.services.product_service import ProductService
from app.infrastructure.repositories.in_memory.in_memory_product_repository import InMemoryProductRepository

container = punq.Container()
# Регистрация зависимостей
container.register(InMemoryProductRepository)
container.register(ProductService, product_repository=InMemoryProductRepository)

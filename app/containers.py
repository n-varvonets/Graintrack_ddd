# app/containers.py

from functools import lru_cache
from punq import Container, Scope

from application.interfaces.product_repository_interface import ProductRepositoryInterface
from application.interfaces.category_repository_interface import CategoryRepositoryInterface
from application.interfaces.reservation_repository_interface import ReservationRepositoryInterface
from application.interfaces.sale_repository_interface import SaleRepositoryInterface

from domain.services.product_service import ProductService
from domain.services.category_service import CategoryService
from domain.services.reservation_service import ReservationService
from domain.services.sale_service import SaleService

from infrastructure.repositories.in_memory.in_memory_product_repository import InMemoryProductRepository
from infrastructure.repositories.in_memory.in_memory_category_repository import InMemoryCategoryRepository
from infrastructure.repositories.in_memory.in_memory_reservation_repository import InMemoryReservationRepository
from infrastructure.repositories.in_memory.in_memory_sale_repository import InMemorySaleRepository

@lru_cache(1)
def init_container() -> Container:
    """
    Инициализирует и возвращает контейнер зависимостей.
    Использует lru_cache для обеспечения синглтон поведения.
    """
    container = Container()

    container.register(ProductRepositoryInterface, InMemoryProductRepository, scope=Scope.singleton)
    container.register(CategoryRepositoryInterface, InMemoryCategoryRepository, scope=Scope.singleton)
    container.register(ReservationRepositoryInterface, InMemoryReservationRepository, scope=Scope.singleton)
    container.register(SaleRepositoryInterface, InMemorySaleRepository, scope=Scope.singleton)

    # Регистрация сервисов с их зависимостями через интерфейсы
    container.register(ProductService,
                       product_repository=ProductRepositoryInterface,
                       reservation_service=ReservationService,
                       sale_service=SaleService,
                       scope=Scope.singleton)

    container.register(CategoryService,
                       category_repository=CategoryRepositoryInterface,
                       scope=Scope.singleton)

    container.register(ReservationService,
                       reservation_repository=ReservationRepositoryInterface,
                       product_repository=ProductRepositoryInterface,
                       scope=Scope.singleton)

    container.register(SaleService,
                       sale_repository=SaleRepositoryInterface,
                       product_repository=ProductRepositoryInterface,
                       scope=Scope.singleton)

    return container

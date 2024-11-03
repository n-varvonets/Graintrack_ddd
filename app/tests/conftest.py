# app/tests/conftest.py

import pytest
from punq import Container

# Import interfaces
from app.application.interfaces.product_repository_interface import ProductRepositoryInterface
from app.application.interfaces.category_repository_interface import CategoryRepositoryInterface
from app.application.interfaces.reservation_repository_interface import ReservationRepositoryInterface
from app.application.interfaces.sale_repository_interface import SaleRepositoryInterface

# Import services
from app.domain.services.product_service import ProductService
from app.domain.services.category_service import CategoryService
from app.domain.services.reservation_service import ReservationService
from app.domain.services.sale_service import SaleService

# Import in-memory repositories
from app.infrastructure.repositories.in_memory.in_memory_product_repository import InMemoryProductRepository
from app.infrastructure.repositories.in_memory.in_memory_category_repository import InMemoryCategoryRepository
from app.infrastructure.repositories.in_memory.in_memory_reservation_repository import InMemoryReservationRepository
from app.infrastructure.repositories.in_memory.in_memory_sale_repository import InMemorySaleRepository


@pytest.fixture(scope='session')
def test_container():
    container = Container()
    # Register interfaces with their implementations
    container.register(ProductRepositoryInterface, InMemoryProductRepository)
    container.register(CategoryRepositoryInterface, InMemoryCategoryRepository)
    container.register(ReservationRepositoryInterface, InMemoryReservationRepository)
    container.register(SaleRepositoryInterface, InMemorySaleRepository)

    # Register services with their dependencies (using interfaces)
    container.register(ProductService, product_repository=ProductRepositoryInterface)
    container.register(CategoryService, category_repository=CategoryRepositoryInterface)
    container.register(ReservationService, reservation_repository=ReservationRepositoryInterface,
                       product_repository=ProductRepositoryInterface)
    container.register(SaleService, sale_repository=SaleRepositoryInterface,
                       product_repository=ProductRepositoryInterface)

    return container


@pytest.fixture
def product_service(test_container):
    return test_container.resolve(ProductService)


@pytest.fixture
def category_service(test_container):
    return test_container.resolve(CategoryService)


@pytest.fixture
def reservation_service(test_container):
    return test_container.resolve(ReservationService)


@pytest.fixture
def sale_service(test_container):
    return test_container.resolve(SaleService)


@pytest.fixture
def product_repository(test_container):
    return test_container.resolve(ProductRepositoryInterface)


@pytest.fixture
def category_repository(test_container):
    return test_container.resolve(CategoryRepositoryInterface)


@pytest.fixture
def reservation_repository(test_container):
    return test_container.resolve(ReservationRepositoryInterface)


@pytest.fixture
def sale_repository(test_container):
    return test_container.resolve(SaleRepositoryInterface)

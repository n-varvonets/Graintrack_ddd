import pytest
from app.infrastructure.repositories.in_memory.in_memory_product_repository import InMemoryProductRepository
from app.infrastructure.repositories.in_memory.in_memory_category_repository import InMemoryCategoryRepository
from app.infrastructure.repositories.in_memory.in_memory_reservation_repository import InMemoryReservationRepository
from app.infrastructure.repositories.in_memory.in_memory_sale_repository import InMemorySaleRepository
from app.domain.services.product_service import ProductService
from app.domain.services.category_service import CategoryService
from app.domain.services.reservation_service import ReservationService
from app.domain.services.sale_service import SaleService

@pytest.fixture
def product_repository():
    return InMemoryProductRepository()

@pytest.fixture
def category_repository():
    return InMemoryCategoryRepository()

@pytest.fixture
def reservation_repository():
    return InMemoryReservationRepository()

@pytest.fixture
def sale_repository():
    return InMemorySaleRepository()

@pytest.fixture
def reservation_service(reservation_repository):
    return ReservationService(reservation_repository)

@pytest.fixture
def sale_service(sale_repository):
    return SaleService(sale_repository)

@pytest.fixture
def product_service(product_repository, reservation_service, sale_service):
    return ProductService(product_repository, reservation_service, sale_service)

@pytest.fixture
def category_service(category_repository):
    return CategoryService(category_repository)

import pytest
import pytest_asyncio
from httpx import AsyncClient
from punq import Container, Scope

# Import interfaces
from application.interfaces.product_repository_interface import ProductRepositoryInterface
from application.interfaces.category_repository_interface import CategoryRepositoryInterface
from application.interfaces.reservation_repository_interface import ReservationRepositoryInterface
from application.interfaces.sale_repository_interface import SaleRepositoryInterface

# Impservices
from domain.services.product_service import ProductService
from domain.services.category_service import CategoryService
from domain.services.reservation_service import ReservationService
from domain.services.sale_service import SaleService

# Impin-memory repositories
from infrastructure.repositories.in_memory.in_memory_product_repository import InMemoryProductRepository
from infrastructure.repositories.in_memory.in_memory_category_repository import InMemoryCategoryRepository
from infrastructure.repositories.in_memory.in_memory_reservation_repository import InMemoryReservationRepository
from infrastructure.repositories.in_memory.in_memory_sale_repository import InMemorySaleRepository
from main import create_app


@pytest.fixture(scope='session')
def test_container():
    container = Container()
    # Регистрация интерфейсов с реализациями в режиме singleton
    container.register(ProductRepositoryInterface, InMemoryProductRepository, scope=Scope.singleton)
    container.register(CategoryRepositoryInterface, InMemoryCategoryRepository, scope=Scope.singleton)
    container.register(ReservationRepositoryInterface, InMemoryReservationRepository, scope=Scope.singleton)
    container.register(SaleRepositoryInterface, InMemorySaleRepository, scope=Scope.singleton)

    # Регистрация сервисов с их зависимостями через интерфейсы
    container.register(ProductService, product_repository=ProductRepositoryInterface, scope=Scope.singleton)
    container.register(CategoryService, category_repository=CategoryRepositoryInterface, scope=Scope.singleton)
    container.register(ReservationService, reservation_repository=ReservationRepositoryInterface,
                       product_repository=ProductRepositoryInterface, scope=Scope.singleton)
    container.register(SaleService, sale_repository=SaleRepositoryInterface,
                       product_repository=ProductRepositoryInterface, scope=Scope.singleton)

    return container


# Дополнительные фикстуры для удобства (опционально)
@pytest.fixture(scope='session')
def product_service(test_container):
    return test_container.resolve(ProductService)

@pytest.fixture(scope='function')
def category_service(category_repository):
    return CategoryService(category_repository=category_repository)

@pytest.fixture
def reservation_service(test_container):
    return test_container.resolve(ReservationService)

@pytest.fixture
def sale_service(test_container):
    return test_container.resolve(SaleService)

@pytest.fixture(scope='session')
def product_repository(test_container):
    return test_container.resolve(ProductRepositoryInterface)

@pytest.fixture(scope='function')
def category_repository(test_container):
    repository = test_container.resolve(CategoryRepositoryInterface)
    repository.clear()
    return repository


@pytest.fixture
def reservation_repository(test_container):
    return test_container.resolve(ReservationRepositoryInterface)

@pytest.fixture
def sale_repository(test_container):
    return test_container.resolve(SaleRepositoryInterface)


@pytest_asyncio.fixture(scope='session')
async def async_client(test_container):
    # Создаём приложение с использованием тестового контейнера
    app = create_app(container=test_container)

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

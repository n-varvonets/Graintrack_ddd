## Сущности и их взаимодействия:

- **Category**: представляет категорию товара. Категория может иметь родительскую категорию (для подкатегорий).

- **Product**: представляет товар. Содержит ссылку на категорию через `category_id`, имеет цену (`price`), количество на складе (`stock`), скидку (`discount`).

- **Reservation**: представляет резервирование товара. Связана с продуктом через `product_id`.

- **Sale**: представляет продажу товара. Также связана с продуктом через `product_id`.

```python
# Импортируем необходимые классы
from domain.entities.category import Category
from domain.entities.product import Product
from domain.values.price import Price
from domain.values.quantity import Quantity
from domain.values.discount import Discount
import uuid

# Создаем категорию
category = Category(
    name="Electronics",
    parent_category_id=None  # Это корневая категория
)

# Сохраняем категорию в репозиторий
from infrastructure.repositories.in_memory.in_memory_category_repository import InMemoryCategoryRepository

category_repository = InMemoryCategoryRepository()
category_repository.add(category)

# Создаем продукт
product = Product(
    name="Smartphone",
    category_id=category.oid,  # Используем идентификатор категории
    price=Price(999.99),
    stock=Quantity(50),
    discount=Discount(10.0)  # Скидка 10%
)

# Сохраняем продукт в репозиторий
from infrastructure.repositories.in_memory.in_memory_product_repository import InMemoryProductRepository

product_repository = InMemoryProductRepository()
product_repository.add(product)

# Проверяем доступность продукта
print(product.is_available())  # Должно вывести True

# Получаем цену после скидки
print(product.get_price_after_discount())  # Должно вывести цену со скидкой

# Резервируем товар через сервис
from domain.services.reservation_service import ReservationService
from infrastructure.repositories.in_memory.in_memory_reservation_repository import InMemoryReservationRepository

reservation_repository = InMemoryReservationRepository()
reservation_service = ReservationService(reservation_repository)

reservation = reservation_service.create_reservation(
    product_id=product.oid,
    quantity=2
)

# Обновляем остаток товара
product.stock = Quantity(product.stock.value - 2)
product_repository.update(product)

# Продаем товар через сервис
from domain.services.sale_service import SaleService
from infrastructure.repositories.in_memory.in_memory_sale_repository import InMemorySaleRepository

sale_repository = InMemorySaleRepository()
sale_service = SaleService(sale_repository)

sale = sale_service.record_sale(
    product_id=product.oid,
    quantity=2
)

# Обновляем остаток товара после продажи
product.stock = Quantity(product.stock.value - 2)
product_repository.update(product)
```

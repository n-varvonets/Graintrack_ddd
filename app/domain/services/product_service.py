# app/domain/services/product_service.py

from typing import List, Optional
from app.domain.entities.product import Product
from app.domain.values.price import Price
from app.domain.values.discount import Discount
from app.domain.values.quantity import Quantity
from app.application.interfaces.product_repository_interface import ProductRepositoryInterface
from app.domain.exceptions.product_exceptions import ProductNotFoundException, InvalidDiscountException, InsufficientStockException
from app.domain.services.reservation_service import ReservationService
from app.domain.services.sale_service import SaleService


class ProductService:
    def __init__(
        self,
        product_repository: ProductRepositoryInterface,
        reservation_service: ReservationService,
        sale_service: SaleService
    ):
        self.product_repository = product_repository
        self.reservation_service = reservation_service
        self.sale_service = sale_service

    def create_product(self, product: Product) -> Product:
        """
        Создает новый продукт в системе.
        """
        return self.product_repository.add(product)

    def update_price(self, product_id: str, new_price: Price) -> Product:
        """
        Обновляет цену существующего продукта.
        """
        product = self.get_product_by_id(product_id)
        product.price = new_price
        self.product_repository.update(product)
        return product

    def start_promotion(self, product_id: str, discount_percentage: float) -> Product:
        """
        Запускает акцию на продукт с указанным процентом скидки.
        """
        if not (0 <= discount_percentage <= 100):
            raise InvalidDiscountException(discount_percentage=discount_percentage)
        product = self.get_product_by_id(product_id)
        product.apply_discount(discount_percentage)
        self.product_repository.update(product)
        return product

    def reserve_product(self, product_id: str, quantity: int) -> None:
        """
        Резервирует определенное количество товара.
        """
        product = self.get_product_by_id(product_id)
        if product.stock.value < quantity:
            raise InsufficientStockException(
                product_id=product_id,
                requested_quantity=quantity,
                available_stock=product.stock.value
            )
        product.stock = Quantity(product.stock.value - quantity)
        self.product_repository.update(product)
        self.reservation_service.create_reservation(product_id, quantity)

    def cancel_reservation(self, reservation_id: str) -> None:
        """
        Отменяет резервирование товара.
        """
        reservation = self.reservation_service.get_reservation_by_id(reservation_id)
        product = self.get_product_by_id(reservation.product_id)
        product.stock = Quantity(product.stock.value + reservation.quantity)
        self.product_repository.update(product)
        self.reservation_service.cancel_reservation(reservation_id)

    def sell_product(self, product_id: str, quantity: int) -> None:
        """
        Продает товар и уменьшает количество в наличии.
        """
        product = self.get_product_by_id(product_id)
        if product.stock.value < quantity:
            raise InsufficientStockException(
                product_id=product_id,
                requested_quantity=quantity,
                available_stock=product.stock.value
            )
        product.stock = Quantity(product.stock.value - quantity)
        self.product_repository.update(product)
        self.sale_service.record_sale(product_id, quantity)

    def get_available_products(self, category_id: Optional[str] = None) -> List[Product]:
        """
        Получает список доступных продуктов, где stock > 0.
        Если указан category_id, фильтрует по категории.
        """
        products = self.product_repository.get_all()
        available_products = [p for p in products if p.stock.value > 0]
        if category_id:
            available_products = [p for p in available_products if p.category_id == category_id]
        return available_products

    def delete_product(self, product_id: str) -> None:
        """
        Удаляет продукт из системы.
        """
        self.product_repository.delete(product_id)

    def get_product_by_id(self, product_id: str) -> Product:
        """
        Получает продукт по его идентификатору.
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id=product_id)
        return product

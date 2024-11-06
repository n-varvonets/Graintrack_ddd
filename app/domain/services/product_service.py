# app/domain/services/product_service.py

from typing import List, Optional, Union
import uuid

from fastapi import Depends, HTTPException
from pydantic import ValidationError

from domain.entities.product import Product
from domain.values.price import Price
from domain.values.discount import Discount
from domain.values.quantity import Quantity
from application.interfaces.product_repository_interface import ProductRepositoryInterface
from domain.exceptions.product_exceptions import (
    ProductNotFoundException,
    InvalidDiscountException,
    InsufficientStockException,
)
from domain.services.reservation_service import ReservationService
from domain.services.sale_service import SaleService
from domain.entities.reservation import Reservation
from domain.entities.sale import Sale
from infrastructure.converters.product_converters import convert_product_to_dto, convert_dto_to_product
from presentation.schemas.product_schema import ProductCreateRequest, ProductUpdateRequest, ProductResponse


class ProductService:
    def __init__(
        self,
        product_repository: ProductRepositoryInterface,
        reservation_service: ReservationService,
        sale_service: SaleService,
    ):
        self.product_repository = product_repository
        self.reservation_service = reservation_service
        self.sale_service = sale_service

    async def create_product(self, product_data: Union[ProductCreateRequest, Product]) -> Product:
        """
        Создает новый продукт в системе.
        """
        product = self._process_product_input(product_data)

        created_product = await self.product_repository.add(product)
        return convert_product_to_dto(created_product)

    async def update_price(self, product_id: str, new_price: Price) -> Product:
        """
        Обновляет цену существующего продукта.
        """
        product = await self.get_product_by_id(product_id)
        product.price = new_price
        await self.product_repository.update(product)
        return product

    async def start_promotion(
            self,
            discount_percentage: float,
            product_id: Union[str | uuid.UUID],
    ) -> Union[ProductResponse, InvalidDiscountException, HTTPException]:
        if isinstance(product_id, uuid.UUID):
            product_id = str(product_id)

        if not (0 <= discount_percentage <= 100):
            raise InvalidDiscountException(discount_percentage=discount_percentage)

        product = await self.product_repository.get_by_id(product_id)
        if not isinstance(product, Product):
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")

        product.apply_discount(discount_percentage)
        self.product_repository.update(product)

        return convert_product_to_dto(product)

    async def reserve_product(self, product_id: str, quantity: int) -> None:
        """
        Резервирует определенное количество товара.
        """

        product = await self.product_repository.get_by_id(product_id)
        if product.stock.value < quantity:
            raise InsufficientStockException(
                product_id=product_id,
                requested_quantity=quantity,
                available_stock=product.stock.value,
            )
        product.stock = Quantity(product.stock.value - quantity)
        await self.product_repository.update(product)
        await self.reservation_service.create_reservation(product_id, quantity)

    async def cancel_reservation(self, reservation_id: str) -> None:
        """
        Отменяет резервирование товара.
        """
        reservation = await self.reservation_service.get_reservation_by_id(reservation_id)
        product = await self.get_product_by_id(reservation.product_id)
        product.stock = Quantity(product.stock.value + reservation.quantity)
        await self.product_repository.update(product)
        await self.reservation_service.cancel_reservation(reservation_id)

    async def sell_product(self, product_id: str, quantity: int) -> None:
        """
        Продает товар и уменьшает количество в наличии.
        """
        if isinstance(product_id, uuid.UUID):
            product_id = str(product_id)

        product = await self.product_repository.get_by_id(product_id)
        if product.stock.value < quantity:
            raise InsufficientStockException(
                product_id=product_id,
                requested_quantity=quantity,
                available_stock=product.stock.value,
            )
        product.stock = Quantity(product.stock.value - quantity)
        await self.product_repository.update(product)
        await self.sale_service.record_sale(product_id, quantity)

    async def update_product(self, product_id: str, product_update: ProductUpdateRequest) -> Product:
        product = await self.get_product_by_id(product_id)
        update_data = product_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)
        updated_product = await self.product_repository.update(product)
        return convert_product_to_dto(updated_product)

    async def get_available_products(self, category_id: Optional[str] = None) -> List[Product]:
        """
        Получает список доступных продуктов, где stock > 0.
        Если указан category_id, фильтрует по категории.
        """
        products = await self.product_repository.get_all()
        available_products = [p for p in products if p.stock_value > 0]
        if category_id:
            available_products = [p for p in available_products if p.category_id == category_id]
        return available_products

    async def delete_product(self, product_id: str) -> None:
        """
        Удаляет продукт из системы.
        """
        await self.product_repository.delete(product_id)

    async def get_product_by_id(self, product_id: str) -> Product:
        """
        Получает продукт по его идентификатору.
        """
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id=product_id)
        return convert_product_to_dto(product)

    def _process_product_input(self, product_data: Union[ProductCreateRequest, Product, ProductUpdateRequest, dict]) -> \
    Union[Product, ProductUpdateRequest]:
        """
        Проверяет тип входного продукта и выполняет преобразование в сущность Product или ProductUpdateRequest,
        если переданы соответствующие DTO или dict.
        """
        if isinstance(product_data, ProductCreateRequest):
            return convert_dto_to_product(product_data)
        elif isinstance(product_data, Product):
            return product_data
        elif isinstance(product_data, ProductUpdateRequest):
            return product_data
        elif isinstance(product_data, dict):
            try:
                return ProductUpdateRequest(**product_data)
            except ValidationError as e:
                raise TypeError(f"Invalid product_update data: {e}")
        else:
            raise TypeError(
                "Invalid type for product_data. Expected ProductCreateRequest, Product, ProductUpdateRequest, or dict.")



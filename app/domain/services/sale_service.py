# app/domain/services/sale_service.py

from typing import List, Optional
from datetime import datetime
from domain.entities.sale import Sale
from application.interfaces.sale_repository_interface import SaleRepositoryInterface
from domain.exceptions.sale_exceptions import SaleNotFoundException


class SaleService:
    def __init__(self, sale_repository: SaleRepositoryInterface):
        self.sale_repository = sale_repository

    def record_sale(self, product_id: str, quantity: int) -> Sale:
        """
        Регистрирует продажу товара.
        """
        sale = Sale(
            product_id=product_id,
            quantity=quantity
        )
        return self.sale_repository.add(sale)

    def get_sales_report(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Sale]:
        """
        Получает отчет о продажах за указанный период.
        """
        return self.sale_repository.get_sales_between_dates(start_date, end_date)

    def get_sales_by_product(self, product_id: str) -> List[Sale]:
        """
        Получает список продаж для заданного продукта.
        """
        return self.sale_repository.get_by_product_id(product_id)

    def get_by_id(self, sale_id):
        sale = self.sale_repository.get_by_id(sale_id)
        if sale is None:
            raise SaleNotFoundException(f"Sale with id {sale_id} not found.")
        return sale






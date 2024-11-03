# app/infrastructure/repositories/in_memory/in_memory_sale_repository.py

from typing import List, Optional
from datetime import datetime
from app.domain.entities.sale import Sale
from app.application.interfaces.sale_repository_interface import SaleRepositoryInterface
from app.domain.exceptions.sale_exceptions import SaleNotFoundException

class InMemorySaleRepository(SaleRepositoryInterface):
    def __init__(self):
        self.sales = {}

    def add(self, sale: Sale) -> Sale:
        self.sales[sale.oid] = sale
        return sale

    def get_by_id(self, sale_id: str) -> Optional[Sale]:
        sale = self.sales.get(sale_id)
        if not sale:
            raise SaleNotFoundException(sale_id=sale_id)
        return sale

    def delete(self, sale_id: str) -> None:
        if sale_id not in self.sales:
            raise SaleNotFoundException(sale_id=sale_id)
        del self.sales[sale_id]

    def get_all(self) -> List[Sale]:
        return list(self.sales.values())

    def get_by_product_id(self, product_id: str) -> List[Sale]:
        return [
            sale for sale in self.sales.values()
            if sale.product_id == product_id
        ]

    def get_sales_between_dates(
        self,
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> List[Sale]:
        sales = self.sales.values()
        if start_date:
            sales = filter(lambda s: s.sale_date >= start_date, sales)
        if end_date:
            sales = filter(lambda s: s.sale_date <= end_date, sales)
        return list(sales)

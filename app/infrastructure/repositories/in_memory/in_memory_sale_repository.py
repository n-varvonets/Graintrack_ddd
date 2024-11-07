# app/infrastructure/repositories/in_memory/in_memory_sale_repository.py

from typing import List, Optional
from datetime import datetime
from domain.entities.sale import Sale
from application.interfaces.sale_repository_interface import SaleRepositoryInterface
from domain.exceptions.sale_exceptions import SaleNotFoundException


class InMemorySaleRepository(SaleRepositoryInterface):
    def __init__(self):
        self.sales = {}

    async def add(self, sale: Sale) -> Sale:
        self.sales[sale.oid] = sale
        return sale

    async def get_by_id(self, sale_id: str) -> Optional[Sale]:
        sale = self.sales.get(sale_id)
        if not sale:
            raise SaleNotFoundException(sale_id=sale_id)
        return sale

    async def delete(self, sale_id: str) -> None:
        if sale_id not in self.sales:
            raise SaleNotFoundException(sale_id=sale_id)
        del self.sales[sale_id]

    async def get_all(self) -> List[Sale]:
        return list(self.sales.values())

    async def get_by_product_id(self, product_id: str) -> List[Sale]:
        return [
            sale for sale in self.sales.values()
            if sale.product_id == product_id
        ]

    async def get_sales_between_dates(
            self, start_date: Optional[datetime],
            end_date: Optional[datetime],
            category_id: Optional[str] = None
    ) -> List[Sale]:
        sales = self.sales.values()
        if start_date:
            sales = filter(lambda s: s.sale_date >= start_date, sales)
        if end_date:
            sales = filter(lambda s: s.sale_date <= end_date, sales)
        if category_id:
            sales = filter(lambda s: s.category_id == category_id, sales)
        return list(sales)


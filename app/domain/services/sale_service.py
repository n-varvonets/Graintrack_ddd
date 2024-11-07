from typing import List, Optional, Union
from datetime import datetime
from domain.entities.sale import Sale
from application.interfaces.sale_repository_interface import SaleRepositoryInterface
from domain.exceptions.sale_exceptions import SaleNotFoundException
from presentation.schemas.sale_schema import SaleCreateRequest, SaleResponse
from infrastructure.converters.sale_converters import convert_sale_to_response


class SaleService:
    def __init__(self, sale_repository: SaleRepositoryInterface):
        self.sale_repository = sale_repository

    async def record_sale(self, sale_data: Union[dict, SaleCreateRequest]) -> SaleResponse:
        if isinstance(sale_data, dict):
            sale_data = SaleCreateRequest(**sale_data)
        elif not isinstance(sale_data, SaleCreateRequest):
            raise ValueError("Invalid data provided for creating a sale")

        sale_instance = Sale(
            product_id=sale_data.product_id,
            quantity=sale_data.quantity
        )
        saved_sale = await self.sale_repository.add(sale_instance)
        return convert_sale_to_response(saved_sale)

    async def get_sales_report(
            self, start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            category_id: Optional[str] = None
    ) -> List[SaleResponse]:
        sales = await self.sale_repository.get_sales_between_dates(start_date, end_date)
        if category_id:
            sales = [sale for sale in sales if sale.category_id == category_id]
        return [convert_sale_to_response(sale) for sale in sales]

    async def get_sales_by_product(self, product_id: str) -> List[SaleResponse]:
        sales = await self.sale_repository.get_by_product_id(product_id)
        return [convert_sale_to_response(sale) for sale in sales]

    async def get_by_id(self, sale_id: str) -> SaleResponse:
        sale = await self.sale_repository.get_by_id(sale_id)
        if sale is None:
            raise SaleNotFoundException(f"Sale with id {sale_id} not found.")
        return convert_sale_to_response(sale)

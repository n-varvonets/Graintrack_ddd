# infrastructure/converters/sale_converters.py

from typing import List
from domain.entities.sale import Sale
from presentation.schemas.sale_schema import SaleResponse


def convert_sales_to_responses(sales: List[Sale]) -> List[SaleResponse]:
    return [
        SaleResponse(
            id=sale.oid,
            product_id=sale.product_id,
            quantity=sale.quantity,
            sale_date=sale.sale_date
        )
        for sale in sales
    ]


def convert_sale_to_response(sale: Sale) -> SaleResponse:
    return SaleResponse(
        id=sale.oid,
        product_id=sale.product_id,
        quantity=sale.quantity,
        sale_date=sale.sale_date
    )

# app/presentation/api/v1/endpoints/sales.py

from typing import List, Optional, Union
from datetime import datetime
import uuid

from fastapi import APIRouter, Depends, HTTPException
from domain.services.sale_service import SaleService
from presentation.schemas.sale_schema import (
    SaleCreateRequest,
    SaleResponse
)
from infrastructure.converters.sale_converters import convert_sales_to_responses
from domain.exceptions.sale_exceptions import ApplicationException
from presentation.api.v1.dependencies import get_sale_service

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)

@router.post("/", response_model=SaleResponse, status_code=201)
async def register_sale(
    sale_create: Union[dict | SaleCreateRequest],
    sale_service: SaleService = Depends(get_sale_service)
):
    try:
        sale = await sale_service.record_sale(sale_create)
        return sale
    except ApplicationException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.get("/", response_model=List[SaleResponse])
async def get_sales(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category_id: Optional[str] = None,
    sale_service: SaleService = Depends(get_sale_service)
):
    try:
        sales = await sale_service.get_sales_report(start_date, end_date, category_id)
        return convert_sales_to_responses(sales)
    except ApplicationException as e:
        raise HTTPException(status_code=400, detail=e.message)

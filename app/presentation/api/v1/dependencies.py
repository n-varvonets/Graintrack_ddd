# app/presentation/api/v1/dependencies.py
import uuid
from typing import Union

from fastapi import Request, Depends
from domain.services.product_service import ProductService
from domain.services.category_service import CategoryService
from domain.services.reservation_service import ReservationService
from domain.services.sale_service import SaleService
from application.utils.id_converter import validate_and_convert_product_id


def get_container(request: Request):
    return request.app.state.container


def get_product_service(container=Depends(get_container)) -> ProductService:
    return container.resolve(ProductService)


def get_category_service(container=Depends(get_container)) -> CategoryService:
    return container.resolve(CategoryService)


def get_reservation_service(container=Depends(get_container)) -> ReservationService:
    return container.resolve(ReservationService)


def get_sale_service(container=Depends(get_container)) -> SaleService:
    return container.resolve(SaleService)


def get_validated_product_id(product_id: Union[str, uuid.UUID]) -> str:
    return validate_and_convert_product_id(product_id)

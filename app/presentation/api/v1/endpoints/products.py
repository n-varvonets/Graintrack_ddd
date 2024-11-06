# app/presentation/api/v1/endpoints/products.py

from typing import List, Optional, Union
import uuid

from infrastructure.converters.product_converters import convert_products_to_responses
from presentation.schemas.product_schema import (
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductResponse
)

from fastapi import APIRouter, Depends, HTTPException

from domain.services.product_service import ProductService
from presentation.api.v1.dependencies import get_product_service, get_validated_product_id
from domain.exceptions.product_exceptions import ApplicationException


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    category_id: Optional[uuid.UUID] = None,
    product_service: ProductService = Depends(get_product_service)
):
    products = await product_service.get_available_products(category_id)
    if not products:
        return []
    return convert_products_to_responses(products)


@router.get("/{product_id}/", response_model=ProductResponse)
async def get_product(
    product_id: str = Depends(get_validated_product_id),
    product_service: ProductService = Depends(get_product_service)
):
    try:
        product = await product_service.get_product_by_id(product_id)
        return product
    except ApplicationException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product_create: ProductCreateRequest,
    product_service: ProductService = Depends(get_product_service)
):
    try:
        product = await product_service.create_product(product_create)
        return product
    except ApplicationException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.put("/{product_id}/", response_model=ProductResponse)
async def update_product(
    product_update: Union[dict | ProductUpdateRequest],
    product_id: str = Depends(get_validated_product_id),
    product_service: ProductService = Depends(get_product_service)
):
    try:
        processed_update = product_service._process_product_input(product_update)
        updated_product = await product_service.update_product(product_id, processed_update)
        return updated_product
    except ApplicationException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.delete("/{product_id}/", status_code=204)
async def delete_product(
    product_id: str = Depends(get_validated_product_id),
    product_service: ProductService = Depends(get_product_service)
):
    try:
        await product_service.delete_product(product_id)
    except ApplicationException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.post("/{product_id}/reserve/", status_code=204)
async def reserve_product(
    quantity: int,
    product_id: str = Depends(get_validated_product_id),
    product_service: ProductService = Depends(get_product_service)
):
    try:
        await product_service.reserve_product(product_id, quantity)
    except ApplicationException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.post("/{product_id}/cancel-reservation/", status_code=204)
async def cancel_reservation(
    reservation_id: str,
    product_service: ProductService = Depends(get_product_service)
):
    try:
        await product_service.cancel_reservation(reservation_id)
    except ApplicationException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.post("/{product_id}/sell/", status_code=204)
async def sell_product(
    quantity: int,
    product_id: str = Depends(get_validated_product_id),
    product_service: ProductService = Depends(get_product_service)
):
    try:
        await product_service.sell_product(product_id, quantity)
    except ApplicationException as e:
        raise HTTPException(status_code=400, detail=e.message)



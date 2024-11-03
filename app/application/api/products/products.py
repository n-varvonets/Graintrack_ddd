# app/application/api/products/products.py
from fastapi import APIRouter, Depends, HTTPException
from app.domain.services.product_service import ProductService
from app.domain.exceptions.product_exceptions import ProductNotFoundException
import uuid


router = APIRouter()

# @router.get("/{product_id}", response_model=ProductResponse)
# def get_product(
#     product_id: uuid.UUID,
#     product_service: ProductService = Depends(get_product_service)
# ):
#     try:
#         product = product_service.get_product_by_id(product_id)
#         return product
#     except ProductNotFoundException as e:
#         raise HTTPException(status_code=404, detail=e.message)

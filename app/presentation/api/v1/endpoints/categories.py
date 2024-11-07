# app/presentation/api/v1/endpoints/categories.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from domain.services.category_service import CategoryService
from presentation.schemas.category_schema import (
    CategoryCreateRequest,
    CategoryUpdateRequest,
    CategoryResponse
)
from infrastructure.converters.category_converters import convert_categories_to_responses, convert_category_to_response
from domain.exceptions.category_exceptions import ApplicationException, CategoryNotFoundException
from presentation.api.v1.dependencies import get_category_service

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    category_create: CategoryCreateRequest,
    category_service: CategoryService = Depends(get_category_service)
):
    try:
        category = await category_service.create_category(category_create)
        return convert_category_to_response(category)
    except ApplicationException as e:
        raise HTTPException(status_code=400, detail=e.message)

@router.patch("/{category_id}/", response_model=CategoryResponse)
async def update_category(
    category_id: str,
    category_update: CategoryUpdateRequest,
    category_service: CategoryService = Depends(get_category_service)
):
    try:
        category = await category_service.update_category(category_id, category_update)
        return convert_category_to_response(category)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except ApplicationException as e:
        raise HTTPException(status_code=400, detail=e.message)

@router.delete("/{category_id}/", status_code=204)
async def delete_category(
    category_id: str,
    category_service: CategoryService = Depends(get_category_service)
):
    try:
        await category_service.delete_category(category_id)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except ApplicationException as e:
        raise HTTPException(status_code=400, detail=e.message)

@router.get("/{category_id}/", response_model=CategoryResponse)
async def get_category(
    category_id: str,
    category_service: CategoryService = Depends(get_category_service)
):
    try:
        category = await category_service.get_category_by_id(category_id)
        return convert_category_to_response(category)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except ApplicationException as e:
        raise HTTPException(status_code=400, detail=e.message)

@router.get("/", response_model=List[CategoryResponse])
async def list_categories(
    category_service: CategoryService = Depends(get_category_service)
):
    try:
        categories = await category_service.get_all_categories()
        return convert_categories_to_responses(categories)
    except ApplicationException as e:
        raise HTTPException(status_code=400, detail=e.message)

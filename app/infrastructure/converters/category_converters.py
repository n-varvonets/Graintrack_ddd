# infrastructure/converters/category_converters.py
from typing import List
from domain.entities.category import Category
from presentation.schemas.category_schema import (
    CategoryResponse,
    CategoryCreateRequest,
    CategoryUpdateRequest
)
from uuid import UUID


def convert_categories_to_responses(categories: List[Category]) -> List[CategoryResponse]:
    return [
        CategoryResponse(
            id=category.oid,
            name=category.name,
            parent_category_id=UUID(category.parent_category_id) if category.parent_category_id else None,
            created_at=category.created_at
        )
        for category in categories
    ]


def convert_category_to_response(category: Category) -> CategoryResponse:
    return CategoryResponse(
        id=category.oid,
        name=category.name,
        parent_category_id=UUID(category.parent_category_id) if category.parent_category_id else None,
        created_at=category.created_at
    )


def convert_create_request_to_category(create_request: CategoryCreateRequest) -> Category:
    return Category(
        name=create_request.name,
        parent_category_id=str(create_request.parent_category_id) if create_request.parent_category_id else None
    )


def convert_update_request_to_category(update_request: CategoryUpdateRequest, existing_category: Category) -> Category:
    """
    Updates an existing category object with values from an update request.
    Only updates attributes that are present and not None in the update request.
    Special handling for 'parent_category_id' to ensure it is stored as a string.

    Parameters:
        update_request (CategoryUpdateRequest): The request object containing update values.
        existing_category (Category): The existing category object to update.

    Returns:
        Category: The updated category object.
    """
    # Dictionary of attributes that might be updated
    attributes_to_update = {
        'name': getattr(update_request, 'name', None),
        'parent_category_id': getattr(update_request, 'parent_category_id', None),
        'price': getattr(update_request, 'price', None),
        'stock': getattr(update_request, 'stock', None),
        'discount': getattr(update_request, 'discount', None)
    }

    # Iterating over the dictionary to update existing category if values are not None
    for attribute, value in attributes_to_update.items():
        if value is not None:
            # Convert parent_category_id to string if it's present
            if attribute == 'parent_category_id':
                setattr(existing_category, attribute, str(value))
            else:
                setattr(existing_category, attribute, value)

    return existing_category


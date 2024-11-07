# tests/domain/services/test_category_service.py

import pytest
from httpx import AsyncClient

from domain.entities.category import Category
from domain.exceptions.category_exceptions import CategoryNotFoundException
import uuid

from domain.services.category_service import CategoryService


@pytest.mark.asyncio
async def test_create_category(category_service):
    """
    Checks that a new category can be successfully created and that the created category
    matches the input data.
    """
    category_data = {
        "name": "Electronics",
        "parent_category_id": None
    }
    category = Category(**category_data)

    created_category = await category_service.create_category(category)

    assert created_category.oid in category_service.category_repository.categories
    assert created_category.name == category.name, "Category name does not match expected value"
    assert created_category.parent_category_id == category.parent_category_id, "Parent category ID does not match expected value"


@pytest.mark.asyncio
async def test_get_category_by_id(category_service):
    """
    Ensures that retrieving a category by its unique identifier returns the correct
    category details.
    """
    category = Category(name="Books")
    await category_service.create_category(category)
    assert category.oid in category_service.category_repository.categories

    fetched_category = await category_service.get_category_by_id(category.oid)
    assert fetched_category == category


@pytest.mark.asyncio
async def test_get_nonexistent_category(category_service):
    """
    Validates that attempting to retrieve a category that does not exist results in
    a CategoryNotFoundException.
    """
    non_existent_category_id = str(uuid.uuid4())
    with pytest.raises(CategoryNotFoundException):
        await category_service.get_category_by_id(non_existent_category_id)


@pytest.mark.asyncio
async def test_get_all_categories(category_service):
    """
    Confirms that retrieving all categories returns the complete list of created
    categories.
    """
    category1 = Category(name="Fashion")
    category2 = Category(name="Home")
    await category_service.create_category(category1)
    await category_service.create_category(category2)
    categories = await category_service.get_all_categories()
    assert len(categories) == 2
    assert category1 in categories and category2 in categories

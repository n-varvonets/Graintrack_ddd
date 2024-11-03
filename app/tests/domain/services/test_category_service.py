# tests/domain/services/test_category_service.py

import pytest
from app.domain.services.category_service import CategoryService
from app.domain.entities.category import Category
from app.domain.exceptions.category_exceptions import CategoryNotFoundException
import uuid


def test_create_category(category_service):
    category = Category(name="Electronics")
    created_category = category_service.create_category(category)
    assert created_category == category


def test_get_category_by_id(category_service):
    category = Category(name="Books")
    category_service.create_category(category)
    fetched_category = category_service.get_category_by_id(category.oid)
    assert fetched_category == category


def test_get_nonexistent_category(category_service):
    non_existent_category_id = str(uuid.uuid4())
    with pytest.raises(CategoryNotFoundException):
        category_service.get_category_by_id(non_existent_category_id)


def test_get_all_categories(category_service):
    category1 = Category(name="Fashion")
    category2 = Category(name="Home")
    category_service.create_category(category1)
    category_service.create_category(category2)
    categories = category_service.get_all_categories()
    assert len(categories) == 2
    assert category1 in categories and category2 in categories

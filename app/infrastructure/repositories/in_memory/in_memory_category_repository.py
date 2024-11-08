# app/infrastructure/repositories/in_memory/in_memory_category_repository.py

from typing import List, Optional
from domain.entities.category import Category
from application.interfaces.category_repository_interface import CategoryRepositoryInterface
from domain.exceptions.category_exceptions import CategoryNotFoundException


class InMemoryCategoryRepository(CategoryRepositoryInterface):
    def __init__(self):
        self.categories = {}

    def add(self, category: Category) -> Category:
        self.categories[category.oid] = category
        return category

    async def get_by_id(self, category_id: str) -> Optional[Category]:
        category = self.categories.get(category_id)
        if not category:
            raise CategoryNotFoundException(category_id)
        return category

    async def update(self, category: Category) -> None:
        if category.oid not in self.categories:
            raise CategoryNotFoundException(category_id=category.oid)
        self.categories[category.oid] = category

    async def delete(self, category_id: str) -> None:
        if category_id not in self.categories:
            raise CategoryNotFoundException(category_id=category_id)
        del self.categories[category_id]

    async def get_all(self) -> List[Category]:
        return list(self.categories.values())

    def get_subcategories(self, parent_category_id: str) -> List[Category]:
        return [
            category for category in self.categories.values()
            if category.parent_category_id == parent_category_id
        ]

    def clear(self):
        self.categories.clear()

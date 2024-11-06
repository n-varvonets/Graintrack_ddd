# app/domain/services/category_service.py

from typing import List, Optional
from domain.entities.category import Category
from application.interfaces.category_repository_interface import CategoryRepositoryInterface
from domain.exceptions.category_exceptions import CategoryNotFoundException

class CategoryService:
    def __init__(self, category_repository: CategoryRepositoryInterface):
        self.category_repository = category_repository

    def create_category(self, category: Category) -> Category:
        """
        Создает новую категорию.
        """
        return self.category_repository.add(category)

    def update_category(self, category_id: str, name: str, parent_category_id: Optional[str]) -> Category:
        """
        Обновляет существующую категорию.
        """
        category = self.get_category_by_id(category_id)
        category.name = name
        category.parent_category_id = parent_category_id
        self.category_repository.update(category)
        return category

    def delete_category(self, category_id: str) -> None:
        """
        Удаляет категорию.
        """
        self.category_repository.delete(category_id)

    async def get_category_by_id(self, category_id: str) -> Category:
        """
        Получает категорию по ее идентификатору.
        """
        category = await self.category_repository.get_by_id(category_id)
        return category

    def get_all_categories(self) -> List[Category]:
        """
        Получает список всех категорий.
        """
        return self.category_repository.get_all()

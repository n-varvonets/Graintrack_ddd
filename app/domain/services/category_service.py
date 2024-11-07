# domain/services/category_service.py
from typing import List, Optional, Union
from domain.entities.category import Category
from infrastructure.repositories.in_memory.in_memory_category_repository import CategoryRepositoryInterface
from presentation.schemas.category_schema import CategoryCreateRequest, CategoryUpdateRequest
from infrastructure.converters.category_converters import (
    convert_create_request_to_category,
    convert_update_request_to_category, convert_category_to_response
)
from domain.exceptions.category_exceptions import CategoryNotFoundException


class CategoryService:
    def __init__(self, category_repository: CategoryRepositoryInterface):
        """
        Initializes the CategoryService with a repository interface.
        """
        self.category_repository = category_repository

    async def create_category(self, category: Union[CategoryCreateRequest| Category]) -> Category:
        """
        Creates a new category using data provided in the CategoryCreateRequest schema.
        Converts the schema into a Category entity and saves it to the repository.
        """
        if isinstance(category, CategoryCreateRequest):
            category = convert_create_request_to_category(category)
        created_category = self.category_repository.add(category)
        return created_category

    async def update_category(self, category_id: str, category_update: CategoryUpdateRequest) -> Category:
        """
        Updates an existing category identified by category_id with the data provided in the CategoryUpdateRequest.
        Fetches the category, applies updates, and saves the changes back to the repository.
        """
        category = await self.get_category_by_id(category_id)
        updated_category = convert_update_request_to_category(category_update, category)
        await self.category_repository.update(updated_category)
        return updated_category

    async def delete_category(self, category_id: str) -> None:
        """
        Deletes a category from the repository identified by category_id.
        """
        await self.category_repository.delete(category_id)

    async def get_category_by_id(self, category_id: str) -> Category:
        """
        Retrieves a category by its ID from the repository.
        Raises a CategoryNotFoundException if the category is not found.
        """
        category = await self.category_repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundException(category_id=category_id)
        # return convert_category_to_response(category)
        return category

    async def get_all_categories(self) -> List[Category]:
        """
        Returns a list of all categories stored in the repository.
        """
        return await self.category_repository.get_all()

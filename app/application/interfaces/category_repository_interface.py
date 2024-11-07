# app/application/interfaces/category_repository_interface.py

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.category import Category

class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def add(self, category: Category) -> Category:
        """
        Добавляет новую категорию в репозиторий.

        :param category: Экземпляр категории для добавления.
        :return: Добавленная категория.
        """
        pass

    @abstractmethod
    async def get_by_id(self, category_id: str) -> Optional[Category]:
        """
        Получает категорию по ее идентификатору.

        :param category_id: Идентификатор категории.
        :return: Найденная категория или None, если не найдена.
        """
        pass

    @abstractmethod
    def update(self, category: Category) -> None:
        """
        Обновляет информацию о категории в репозитории.

        :param category: Экземпляр категории с обновленными данными.
        """
        pass

    @abstractmethod
    def delete(self, category_id: str) -> None:
        """
        Удаляет категорию из репозитория по ее идентификатору.

        :param category_id: Идентификатор категории для удаления.
        """
        pass

    @abstractmethod
    async def get_all(self) -> List[Category]:
        """
        Получает список всех категорий.

        :return: Список категорий.
        """
        pass

    @abstractmethod
    def get_subcategories(self, parent_category_id: str) -> List[Category]:
        """
        Получает подкатегории для заданной родительской категории.

        :param parent_category_id: Идентификатор родительской категории.
        :return: Список подкатегорий.
        """
        pass

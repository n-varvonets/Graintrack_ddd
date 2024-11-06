# app/application/interfaces/product_repository_interface.py

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.product import Product

class ProductRepositoryInterface(ABC):
    @abstractmethod
    def add(self, product: Product) -> Product:
        """
        Добавляет новый продукт в репозиторий.

        :param product: Экземпляр продукта для добавления.
        :return: Добавленный продукт.
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: str) -> Optional[Product]:
        """
        Получает продукт по его идентификатору.

        :param product_id: Идентификатор продукта.
        :return: Найденный продукт или None, если не найден.
        """
        pass

    @abstractmethod
    def update(self, product: Product) -> None:
        """
        Обновляет информацию о продукте в репозитории.

        :param product: Экземпляр продукта с обновленными данными.
        """
        pass

    @abstractmethod
    def delete(self, product_id: str) -> None:
        """
        Удаляет продукт из репозитория по его идентификатору.

        :param product_id: Идентификатор продукта для удаления.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Product]:
        """
        Получает список всех продуктов.

        :return: Список продуктов.
        """
        pass

    @abstractmethod
    def get_by_category(self, category_id: str) -> List[Product]:
        """
        Получает продукты по идентификатору категории.

        :param category_id: Идентификатор категории.
        :return: Список продуктов в указанной категории.
        """
        pass

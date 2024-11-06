# app/application/interfaces/sale_repository_interface.py

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from domain.entities.sale import Sale


class SaleRepositoryInterface(ABC):
    @abstractmethod
    def add(self, sale: Sale) -> Sale:
        """
        Добавляет новую запись о продаже в репозиторий.

        :param sale: Экземпляр продажи для добавления.
        :return: Добавленная продажа.
        """
        pass

    @abstractmethod
    def get_by_id(self, sale_id: str) -> Optional[Sale]:
        """
        Получает продажу по ее идентификатору.

        :param sale_id: Идентификатор продажи.
        :return: Найденная продажа или None, если не найдена.
        """
        pass

    @abstractmethod
    def delete(self, sale_id: str) -> None:
        """
        Удаляет запись о продаже из репозитория по ее идентификатору.

        :param sale_id: Идентификатор продажи для удаления.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Sale]:
        """
        Получает список всех продаж.

        :return: Список продаж.
        """
        pass

    @abstractmethod
    def get_by_product_id(self, product_id: str) -> List[Sale]:
        """
        Получает продажи для заданного продукта.

        :param product_id: Идентификатор продукта.
        :return: Список продаж.
        """
        pass

    @abstractmethod
    def get_sales_between_dates(self, start_date: Optional[datetime], end_date: Optional[datetime]) -> List[Sale]:
        """
        Получает продажи в заданном диапазоне дат.

        :param start_date: Начальная дата диапазона.
        :param end_date: Конечная дата диапазона.
        :return: Список продаж в указанном диапазоне.
        """
        pass

# app/application/interfaces/reservation_repository_interface.py

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.reservation import Reservation


class ReservationRepositoryInterface(ABC):
    @abstractmethod
    async def add(self, reservation: Reservation) -> Reservation:
        """
        Добавляет новое резервирование в репозиторий.

        :param reservation: Экземпляр резервирования для добавления.
        :return: Добавленное резервирование.
        """
        pass

    @abstractmethod
    def get_by_id(self, reservation_id: str) -> Optional[Reservation]:
        """
        Получает резервирование по его идентификатору.

        :param reservation_id: Идентификатор резервирования.
        :return: Найденное резервирование или None, если не найдено.
        """
        pass

    @abstractmethod
    def update(self, reservation: Reservation) -> None:
        """
        Обновляет информацию о резервировании в репозитории.

        :param reservation: Экземпляр резервирования с обновленными данными.
        """
        pass

    @abstractmethod
    def delete(self, reservation_id: str) -> None:
        """
        Удаляет резервирование из репозитория по его идентификатору.

        :param reservation_id: Идентификатор резервирования для удаления.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Reservation]:
        """
        Получает список всех резервирований.

        :return: Список резервирований.
        """
        pass

    @abstractmethod
    def get_by_product_id(self, product_id: str) -> List[Reservation]:
        """
        Получает резервирования для заданного продукта.

        :param product_id: Идентификатор продукта.
        :return: Список резервирований.
        """
        pass

    @abstractmethod
    def get_active_reservations(self) -> List[Reservation]:
        """
        Получает все активные (не отмененные) резервирования.

        :return: Список активных резервирований.
        """
        pass

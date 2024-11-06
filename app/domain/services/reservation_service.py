# app/domain/services/reservation_service.py

from typing import List
from domain.entities.reservation import Reservation
from application.interfaces.reservation_repository_interface import ReservationRepositoryInterface
from domain.exceptions.reservation_exceptions import ReservationNotFoundException


class ReservationService:
    def __init__(self, reservation_repository: ReservationRepositoryInterface):
        self.reservation_repository = reservation_repository

    def create_reservation(self, product_id: str, quantity: int) -> Reservation:
        """
        Создает новое резервирование товара.
        """
        reservation = Reservation(
            product_id=product_id,
            quantity=quantity
        )
        return self.reservation_repository.add(reservation)

    def cancel_reservation(self, reservation_id: str) -> None:
        """
        Отменяет резервирование.
        """
        reservation = self.get_reservation_by_id(reservation_id)
        reservation.cancel()
        self.reservation_repository.update(reservation)

    def get_reservation_by_id(self, reservation_id: str) -> Reservation:
        """
        Получает резервирование по его идентификатору.
        """
        reservation = self.reservation_repository.get_by_id(reservation_id)
        if not reservation:
            raise ReservationNotFoundException(reservation_id=reservation_id)
        return reservation

    def get_reservations_by_product(self, product_id: str) -> List[Reservation]:
        """
        Получает все резервирования для заданного продукта.
        """
        return self.reservation_repository.get_by_product_id(product_id)

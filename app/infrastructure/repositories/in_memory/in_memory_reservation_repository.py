# app/infrastructure/repositories/in_memory/in_memory_reservation_repository.py

from typing import List, Optional
from app.domain.entities.reservation import Reservation
from app.application.interfaces.reservation_repository_interface import ReservationRepositoryInterface
from app.domain.exceptions.reservation_exceptions import ReservationNotFoundException


class InMemoryReservationRepository(ReservationRepositoryInterface):
    def __init__(self):
        self.reservations = {}

    def add(self, reservation: Reservation) -> Reservation:
        self.reservations[reservation.oid] = reservation
        return reservation

    def get_by_id(self, reservation_id: str) -> Optional[Reservation]:
        reservation = self.reservations.get(reservation_id)
        if not reservation:
            raise ReservationNotFoundException(reservation_id=reservation_id)
        return reservation

    def update(self, reservation: Reservation) -> None:
        if reservation.oid not in self.reservations:
            raise ReservationNotFoundException(reservation_id=reservation.oid)
        self.reservations[reservation.oid] = reservation

    def delete(self, reservation_id: str) -> None:
        if reservation_id not in self.reservations:
            raise ReservationNotFoundException(reservation_id=reservation_id)
        del self.reservations[reservation_id]

    def get_all(self) -> List[Reservation]:
        return list(self.reservations.values())

    def get_by_product_id(self, product_id: str) -> List[Reservation]:
        return [
            reservation for reservation in self.reservations.values()
            if reservation.product_id == product_id
        ]

    def get_active_reservations(self) -> List[Reservation]:
        return [
            reservation for reservation in self.reservations.values()
            if reservation.status == "reserved"
        ]

# app/domain/services/reservation_service.py

from typing import List
from domain.entities.reservation import Reservation
from application.interfaces.reservation_repository_interface import ReservationRepositoryInterface
from domain.exceptions.reservation_exceptions import ReservationNotFoundException
from infrastructure.converters.reservation_converters import convert_reservation_to_response, \
    convert_reservations_to_responses


class ReservationService:
    def __init__(self, reservation_repository: ReservationRepositoryInterface):
        self.reservation_repository = reservation_repository

    async def create_reservation(self, reservation: dict) -> Reservation:
        """
        Creates a new reservation for a product and returns the reservation data as a DTO.
        """
        if not isinstance(reservation, dict) or "product_id" not in reservation or "quantity" not in reservation:
            raise ValueError("Missing 'product_id' or 'quantity' in reservation data.")

        reservation_instance = Reservation(
            product_id=reservation["product_id"],
            quantity=reservation["quantity"]
        )
        saved_reservation = await self.reservation_repository.add(reservation_instance)
        return convert_reservation_to_response(saved_reservation)

    async def cancel_reservation(self, reservation_id: str) -> None:
        reservation = self.reservation_repository.get_by_id(reservation_id)
        reservation.cancel()
        self.reservation_repository.update(reservation)

    async def get_reservation_by_id(self, reservation_id: str) -> Reservation:
        reservation = self.reservation_repository.get_by_id(reservation_id)
        if not reservation:
            raise ReservationNotFoundException(reservation_id=reservation_id)
        return convert_reservation_to_response(reservation)

    async def get_reservations_by_product(self, product_id: str) -> List[Reservation]:
        reservations = await self.reservation_repository.get_by_product_id(product_id)
        return convert_reservations_to_responses(reservations)

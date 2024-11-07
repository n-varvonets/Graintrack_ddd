# infrastructure/converters/reservation_converters.py

from typing import List
from domain.entities.reservation import Reservation
from presentation.schemas.reservation_schema import ReservationResponse

def convert_reservations_to_responses(reservations: List[Reservation]) -> List[ReservationResponse]:
    return [
        ReservationResponse(
            id=reservation.oid,
            product_id=reservation.product_id,
            quantity=reservation.quantity,
            status=reservation.status,
            created_at=reservation.created_at
        )
        for reservation in reservations
    ]

def convert_reservation_to_response(reservation: Reservation) -> ReservationResponse:
    return ReservationResponse(
        id=reservation.oid,
        product_id=reservation.product_id,
        quantity=reservation.quantity,
        status=reservation.status,
        created_at=reservation.created_at
    )

# app/domain/exceptions/reservation_exceptions.py

from dataclasses import dataclass
import uuid
from domain.exceptions.base_exception import ApplicationException


@dataclass(eq=False)
class ReservationNotFoundException(ApplicationException):
    reservation_id: uuid.UUID

    @property
    def message(self):
        return f"Reservation with ID {self.reservation_id} not found."


@dataclass(eq=False)
class CannotCancelReservationException(ApplicationException):
    reservation_id: uuid.UUID
    status: str

    @property
    def message(self):
        return f"Cannot cancel reservation {self.reservation_id} with status '{self.status}'."



# tests/domain/services/test_reservation_service.py

import pytest
from domain.services.reservation_service import ReservationService
from domain.entities.reservation import Reservation
from domain.exceptions.reservation_exceptions import ReservationNotFoundException
import uuid


def test_create_reservation(reservation_service):
    """
    Verifies that a new reservation can be successfully created with the specified
    product ID and quantity, and that the reservation status is set to "reserved".
    """
    product_id = str(uuid.uuid4())
    reservation = reservation_service.create_reservation(product_id, 2)
    assert reservation.product_id == product_id
    assert reservation.quantity == 2
    assert reservation.status == "reserved"


def test_cancel_reservation(reservation_service):
    """
    Ensures that an existing reservation can be successfully canceled, and that the
    reservation status updates to "cancelled".
    """
    product_id = str(uuid.uuid4())
    reservation = reservation_service.create_reservation(product_id, 2)
    reservation_service.cancel_reservation(reservation.oid)
    updated_reservation = reservation_service.get_reservation_by_id(reservation.oid)
    assert updated_reservation.status == "cancelled"


def test_get_nonexistent_reservation(reservation_service):
    """
    Confirms that attempting to retrieve a reservation that does not exist raises a
    ReservationNotFoundException.
    """
    non_existent_reservation_id = str(uuid.uuid4())
    with pytest.raises(ReservationNotFoundException):
        reservation_service.get_reservation_by_id(non_existent_reservation_id)

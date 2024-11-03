# tests/domain/services/test_reservation_service.py

import pytest
from app.domain.services.reservation_service import ReservationService
from app.domain.entities.reservation import Reservation
from app.domain.exceptions.reservation_exceptions import ReservationNotFoundException
import uuid


def test_create_reservation(reservation_service):
    product_id = str(uuid.uuid4())
    reservation = reservation_service.create_reservation(product_id, 2)
    assert reservation.product_id == product_id
    assert reservation.quantity == 2
    assert reservation.status == "reserved"


def test_cancel_reservation(reservation_service):
    product_id = str(uuid.uuid4())
    reservation = reservation_service.create_reservation(product_id, 2)
    reservation_service.cancel_reservation(reservation.oid)
    updated_reservation = reservation_service.get_reservation_by_id(reservation.oid)
    assert updated_reservation.status == "cancelled"


def test_get_nonexistent_reservation(reservation_service):
    non_existent_reservation_id = str(uuid.uuid4())
    with pytest.raises(ReservationNotFoundException):
        reservation_service.get_reservation_by_id(non_existent_reservation_id)

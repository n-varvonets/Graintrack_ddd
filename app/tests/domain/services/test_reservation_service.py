# tests/domain/services/test_reservation_service.py

import pytest
from domain.exceptions.reservation_exceptions import ReservationNotFoundException
import uuid

from infrastructure.converters.reservation_converters import convert_reservation_to_response


@pytest.mark.asyncio
async def test_create_reservation(reservation_service):
    """
    Verifies that a new reservation can be successfully created with the specified
    product ID and quantity, and that the reservation status is set to "reserved".
    """
    reservation_data = {
        "product_id": str(uuid.uuid4()),
        "quantity": 2
    }
    reservation = await reservation_service.create_reservation(reservation_data)
    assert reservation.product_id == reservation_data["product_id"]
    assert reservation.quantity == reservation_data["quantity"]
    assert reservation.status == "reserved"


@pytest.mark.asyncio
async def test_cancel_reservation(reservation_service):
    """
    Ensures that an existing reservation can be successfully canceled, and that the
    reservation status updates to "cancelled".
    """
    reservation_data = {
        "product_id": str(uuid.uuid4()),
        "quantity": 2
    }
    reservation = await reservation_service.create_reservation(reservation_data)
    await reservation_service.cancel_reservation(reservation.oid)
    updated_reservation = await reservation_service.get_reservation_by_id(reservation.oid)
    assert updated_reservation.status == "cancelled"


@pytest.mark.asyncio
async def test_get_nonexistent_reservation(reservation_service):
    """
    Confirms that attempting to retrieve a reservation that does not exist raises a
    ReservationNotFoundException.
    """
    non_existent_reservation_id = str(uuid.uuid4())
    with pytest.raises(ReservationNotFoundException):
        await reservation_service.get_reservation_by_id(non_existent_reservation_id)

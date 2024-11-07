# app/presentation/api/v1/endpoints/reservations.py
from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from domain.services.reservation_service import ReservationService
from infrastructure.converters.reservation_converters import convert_reservation_to_response
from presentation.schemas.reservation_schema import (
    ReservationCreateRequest,
    ReservationResponse
)
from domain.exceptions.reservation_exceptions import ApplicationException
from presentation.api.v1.dependencies import get_reservation_service

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)


@router.post("/", response_model=ReservationResponse, status_code=201)
async def create_reservation(
    reservation_data: dict,
    reservation_service: ReservationService = Depends(get_reservation_service)
):
    try:
        reservation = await reservation_service.create_reservation(reservation_data)
        return reservation
    except ApplicationException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.delete("/{reservation_id}/", status_code=204)
async def cancel_reservation(
    reservation_id: str,
    reservation_service: ReservationService = Depends(get_reservation_service)
):
    try:
        await reservation_service.cancel_reservation(reservation_id)
    except ApplicationException as e:
        raise HTTPException(status_code=400, detail=e.message)

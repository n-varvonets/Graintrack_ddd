# app/presentation/schemas/reservation_schema.py

from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime

class ReservationBase(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0, example=2)

class ReservationCreateRequest(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    oid: str = Field(..., alias='id')
    status: str = Field(..., example="reserved")  # e.g., "reserved", "cancelled"
    created_at: datetime = Field(..., description="The date and time the reservation was created")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

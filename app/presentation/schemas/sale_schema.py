# app/presentation/schemas/sale_schema.py

from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime

class SaleBase(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0, example=3)

class SaleCreateRequest(SaleBase):
    pass

class SaleResponse(SaleBase):
    oid: uuid.UUID = Field(..., alias='id')
    sale_date: datetime = Field(..., description="The date and time the sale was recorded")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

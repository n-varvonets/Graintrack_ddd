# app/presentation/schemas/product_schema.py

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Union
import uuid


class ProductBase(BaseModel):
    name: str = Field(..., example="Sample Product")
    category_id: uuid.UUID
    price: float
    stock: int


class ProductCreateRequest(ProductBase):
    pass


class ProductUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, example="Updated Product Name")
    category_id: Optional[Union[str, uuid.UUID]] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    discount: Optional[float] = None


class ProductResponse(ProductBase):
    oid: uuid.UUID = Field(..., alias='id')  # Корректное использование алиаса
    discount: Optional[float] = 0.0
    description: Optional[str] = Field(None, example="Full description of the product")
    created_at: Optional[datetime] = Field(None, description="The date and time the product was created")
    price_after_discount: Optional[float] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
import uuid

class CategoryBase(BaseModel):
    name: str = Field(..., example="Electronics")
    parent_category_id: Optional[uuid.UUID] = Field(
        None, example="123e4567-e89b-12d3-a456-426614174000"
    )

class CategoryCreateRequest(CategoryBase):
    pass

class CategoryUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, example="Updated Category Name")
    parent_category_id: Optional[uuid.UUID] = Field(
        None, example="123e4567-e89b-12d3-a456-426614174000"
    )

class CategoryResponse(CategoryBase):
    oid: uuid.UUID = Field(..., alias='id')
    created_at: Optional[datetime] = Field(
        None, description="The date and time the category was created"
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

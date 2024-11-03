# app/domain/entities/category.py

from dataclasses import dataclass
from typing import Optional
from .base_entity import BaseEntity
import uuid

@dataclass
class Category(BaseEntity):
    name: str
    parent_category_id: Optional[uuid.UUID] = None

from dataclasses import dataclass, field
from datetime import datetime
from .base_entity import BaseEntity
import uuid

@dataclass
class Sale(BaseEntity):
    product_id: uuid.UUID
    quantity: int
    sale_date: datetime = field(default_factory=datetime.now)

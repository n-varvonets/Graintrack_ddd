from dataclasses import dataclass, field
from datetime import datetime
from .base_entity import BaseEntity
import uuid

@dataclass
class Reservation(BaseEntity):
    """
    The Reservation entity is used to track the reservation of items.

    Possible values for status: reserved, cancelled
    """
    product_id: uuid.UUID
    quantity: int
    status: str = "reserved"   # can be 'reserved' or 'cancelled'
    reserved_at: datetime = field(default_factory=datetime.now)

    def cancel(self):
        self.status = "cancelled"

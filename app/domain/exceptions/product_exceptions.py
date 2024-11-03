# app/domain/exceptions/product_exceptions.py

from dataclasses import dataclass
import uuid
from app.domain.exceptions.base_exception import ApplicationException


@dataclass(eq=False)
class ProductNotFoundException(ApplicationException):
    product_id: uuid.UUID

    @property
    def message(self):
        return f"Product with ID {self.product_id} not found."


@dataclass(eq=False)
class InvalidDiscountException(ApplicationException):
    discount_percentage: float

    @property
    def message(self):
        return f"Invalid discount percentage: {self.discount_percentage}. Must be between 0 and 100."



@dataclass(eq=False)
class InsufficientStockException(ApplicationException):
    product_id: uuid.UUID
    requested_quantity: int
    available_stock: int

    @property
    def message(self):
        return (f"Insufficient stock for product {self.product_id}. "
                f"Requested {self.requested_quantity}, but only {self.available_stock} available.")


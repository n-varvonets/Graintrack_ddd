# app/domain/exceptions/sale_exceptions.py

from dataclasses import dataclass
import uuid
from domain.exceptions.base_exception import ApplicationException


@dataclass(eq=False)
class SaleNotFoundException(ApplicationException):
    sale_id: uuid.UUID

    @property
    def message(self):
        return f"Sale with ID {self.sale_id} not found."

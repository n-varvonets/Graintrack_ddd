# app/domain/exceptions/category_exceptions.py

from dataclasses import dataclass
import uuid
from app.domain.exceptions.base_exception import ApplicationException


@dataclass(eq=False)
class CategoryNotFoundException(ApplicationException):
    category_id: uuid.UUID

    @property
    def message(self):
        return f"Category with ID {self.category_id} not found."


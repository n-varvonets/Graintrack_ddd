# app/domain/exceptions/category_exceptions.py

from dataclasses import dataclass
import uuid
from domain.exceptions.base_exception import ApplicationException


@dataclass(eq=False)
class CategoryNotFoundException(ApplicationException):
    category_id: str

    @property
    def message(self):
        return f"Category with ID {self.category_id} not found."



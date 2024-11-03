# domain/values/quantity.py
from dataclasses import dataclass

from .base_value_object import BaseValueObject

@dataclass(frozen=True)
class Quantity(BaseValueObject[int]):
    value: int

    def __post_init__(self):
        self.validate()

    def validate(self):
        if self.value <= 0:
            raise ValueError("Quantity must be a positive integer.")

    def as_generic_type(self):
        return str(self.value)
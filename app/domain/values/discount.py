# domain/values/discount.py
from dataclasses import dataclass

from .base_value_object import BaseValueObject

@dataclass(frozen=True)
class Discount(BaseValueObject[float]):
    value: float

    def validate(self):
        if not (0 <= self.value <= 100):
            raise ValueError("Discount must be between 0 and 100 percent.")

    def apply_to(self, price: float) -> float:
        """Apply discount to a given price."""
        return price * (1 - self.value / 100)

    def __post_init__(self):
        self.validate()

    def as_generic_type(self):
        return str(self.value)
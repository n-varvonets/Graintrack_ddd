# domain/values/price.py
from dataclasses import dataclass

from .base_value_object import BaseValueObject

@dataclass(frozen=True)
class Price(BaseValueObject[float]):
    value: float

    def __post_init__(self):
        self.validate()

    def validate(self):
        if self.value < 0:
            raise ValueError("Price must be non-negative.")

    def __str__(self) -> str:
        return f"${self.value:.2f}"

    def as_generic_type(self):
        return str(self.value)
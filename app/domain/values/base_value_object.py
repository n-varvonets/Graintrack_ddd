# domain/values/base_value_object.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

VT = TypeVar("VT", bound=Any)

@dataclass(frozen=True)
class BaseValueObject(ABC, Generic[VT]):
    value: VT

    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self):
        """Enforce specific validation rules for the value object."""
        pass

    def as_generic_type(self) -> VT:
        """Return the value as its generic type."""
        return self.value

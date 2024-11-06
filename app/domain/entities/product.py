# domain/entities/product.py

from dataclasses import dataclass
from typing import Optional
from .base_entity import BaseEntity
from ..values.price import Price
from ..values.quantity import Quantity
from ..values.discount import Discount


@dataclass
class Product(BaseEntity):
    name: str
    category_id: str
    price: Price
    stock: Quantity
    discount: Optional[Discount] = Discount(0.0)

    @property
    def price_value(self) -> float:
        return self.price.value

    @property
    def stock_value(self) -> int:
        return self.stock.value

    @property
    def discount_value(self) -> float:
        return self.discount.value if self.discount else 0.0

    def is_available(self) -> bool:
        """Check if the product is available in stock."""
        return self.stock.value > 0

    def apply_discount(self, discount_percentage: float):
        """Set a discount without altering price directly."""
        self.discount = Discount(discount_percentage)

    def get_price_after_discount(self) -> float:
        return round(self.price.value * (1 - self.discount.value / 100), 2)


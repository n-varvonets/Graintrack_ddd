from abc import ABC
from dataclasses import dataclass, field
import uuid
from datetime import datetime


@dataclass(eq=False)
class BaseEntity(ABC):
    oid: str = field(
        default_factory=lambda: str(uuid.uuid4()),
        kw_only=True
    )
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: "BaseEntity") -> bool:
        if not isinstance(__value, BaseEntity):
            return NotImplemented
        return self.oid == __value.oid

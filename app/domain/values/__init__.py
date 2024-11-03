from dataclasses import dataclass, field
import uuid

@dataclass
class BaseEntity:
    id: uuid.UUID = field(default_factory=uuid.uuid4)

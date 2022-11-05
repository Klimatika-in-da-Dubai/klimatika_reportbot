from dataclasses import dataclass, field


@dataclass
class Report:
    name: str
    phone: int
    email: str
    address: str
    rooms_count: int
    rooms_before: list = field(default_factory=list)
    rooms_after: list = field(default_factory=list)

from dataclasses import dataclass, field


@dataclass
class Report:
    name: str = field(default="")
    phone: int = field(default=0)
    email: str = field(default="")
    address: str = field(default="")
    rooms_count: int = field(default=0)
    rooms_before: list = field(default_factory=list)
    rooms_after: list = field(default_factory=list)

    _room_index: int = field(repr=False, default=0)

    @property
    def room_index(self) -> int:
        return self._room_index

    @room_index.setter
    def room_index(self, value: int) -> None:
        self._room_index = value

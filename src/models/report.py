from dataclasses import dataclass, field
from .room import Room


@dataclass
class Report:
    name: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    comment: str = ""
    rooms_count: int = 0
    rooms: list[Room] = field(default_factory=list)
    additional: list = field(default_factory=list)

    _room_index: int = field(repr=False, default=0)

    @property
    def room_index(self) -> int:
        return self._room_index

    @room_index.setter
    def room_index(self, value: int) -> None:
        self._room_index = value

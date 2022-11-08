from dataclasses import dataclass, field
from datetime import datetime
from .room import Room


@dataclass
class Report:
    date: datetime = datetime.now()
    name: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    helped_with: str = ""
    cleaned: str = ""
    rooms_count: int = 0
    rooms: list[Room] = field(default_factory=list)
    extra: list = field(default_factory=list)

    _room_index: int = field(repr=False, default=0)

    @property
    def room_index(self) -> int:
        return self._room_index

    @room_index.setter
    def room_index(self, value: int) -> None:
        self._room_index = value

    def dict(self) -> dict:
        return {
            "Outline": {
                "date": self.date,
                "name": self.name,
                "phone_number": self.phone,
                "address": self.address,
                "helped_with": self.helped_with,
                "cleaned": self.cleaned,
            },
            "Rooms": {
                "number_of_rooms": self.rooms_count,
                "rooms_list": [room.dict() for room in self.rooms],
            },
            "Extra": self.extra,
        }

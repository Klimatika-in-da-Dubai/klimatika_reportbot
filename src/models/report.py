from dataclasses import dataclass, field
from datetime import datetime
from .room import Room
from .client import Client
from enum import Enum


@dataclass
class Report:
    class Service(str, Enum):
        UNKNOWN = ""
        FULL = "Full Cleaning"
        BASE = "Basic Cleaning"
        WITHOUT_CLEANING = "Without Cleaning"

        def __str__(self) -> str:
            return str(self.value)

        def for_button(self, text: str) -> tuple[str, ...]:
            return (text, self.value)

    class ExtraService(str, Enum):
        UNKNOWN = ""
        THERMAIL_INSULATOR_CHANGE_JOB = "Thermal insulator change job"
        NEW_POLYESTER_FILTERS_INSTALLATION = "New polyester filters installation"
        COLD_FOG_MACHINE_DISINFECTIONS = "Cold fog machine disinfections"
        REPAIR_WORKS = "Repair Works"

        def __str__(self) -> str:
            return str(self.value)

        def for_button(self, text: str) -> tuple[str, ...]:
            return (text, self.value)

    date: datetime = datetime.now()
    client: Client = Client()
    service: Service = Service.UNKNOWN
    extra_services: list[ExtraService] = field(default_factory=list)
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

    async def dict_with_binary(self, bot) -> dict:
        return {
            "Outline": {
                "date": self.date,
                "name": self.client.name,
                "phone_number": self.client.phone,
                "address": self.client.address,
                "helped_with": str(self.service),
                "cleaned": "".join([str(service) for service in self.extra_services]),
            },
            "Rooms": {
                "number_of_rooms": self.rooms_count,
                "rooms_list": [await room.dict_with_binary(bot) for room in self.rooms],
            },
            "Extra": self.extra,
        }

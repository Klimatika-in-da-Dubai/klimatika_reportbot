from dataclasses import dataclass, field
from datetime import datetime
from .room import Room
from .client import Client
from enum import Enum


@dataclass
class Report:
    class Service(str, Enum):
        UNKNOWN = ""
        PREMIUM = "Premium"
        PREMIUM_EXTRA = "Premium + Extra"
        OTHER_REPAIR_SERVICES = "Other Repair Services"

        def __str__(self) -> str:
            return str(self.value)

        def for_button(self, text: str) -> tuple[str, Enum]:
            return (text, self)

    class ExtraService(str, Enum):
        UNKNOWN = ""
        THERMAIL_INSULATOR_CHANGE_JOB = "Thermal insulator change job"
        NEW_POLYESTER_FILTERS_INSTALLATION = "New polyester filters installation"
        COLD_FOG_MACHINE_DISINFECTIONS = "Cold fog machine disinfections"
        REPAIR_WORKS = "Repair Works"

        def __str__(self) -> str:
            return str(self.value)

        def for_button(self, text: str) -> tuple[str, Enum]:
            return (text, self)

    date: datetime = datetime.now()
    client: Client = Client()
    service: Service = Service.UNKNOWN
    description: str = ""
    extra_services: list[ExtraService] = field(default_factory=list)
    other_extra_services: list[str] = field(default_factory=list)
    rooms: list[Room] = field(default_factory=list)

    def __post_init__(self):
        self.add_room()

    def add_room(self):
        self.rooms.append(Room())

    async def dict_with_binary(self, bot) -> dict:
        return {
            "Outline": {
                "date": self.date,
                "name": self.client.name,
                "phone_number": self.client.phone,
                "address": self.client.address,
                "helped_with": str(self.service),
                "cleaned": ", ".join(
                    [str(service) for service in self.extra_services]
                    + [str(service) for service in self.other_extra_services]
                ),
            },
            "Rooms": {
                "number_of_rooms": len(self.rooms),
                "rooms_list": [await room.dict_with_binary(bot) for room in self.rooms],
            },
        }

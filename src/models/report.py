from dataclasses import dataclass, field
from datetime import datetime
from .room import Room
from .client import Client
from enum import IntEnum, auto


@dataclass
class Report:
    class Service(IntEnum):
        UNKNOWN = auto()
        PREMIUM = auto()
        PREMIUM_EXTRA = auto()
        OTHER_REPAIR_SERVICES = auto()

        def __str__(self) -> str:
            return SERVICE_NAMES[self]

        def get_description(self):
            return SERVICE_DESCRIPTION[self]

        def for_button(self, text: str) -> tuple[str, IntEnum]:
            return (text, self)

    class ExtraService(IntEnum):
        UNKNOWN = auto()
        THERMAIL_INSULATOR_CHANGE_JOB = auto()
        NEW_POLYESTER_FILTERS_INSTALLATION = auto()
        COLD_FOG_MACHINE_DISINFECTIONS = auto()
        REPAIR_WORKS = auto()

        def __str__(self) -> str:
            return EXTRA_SERVICE_NAME[self]

        def get_description(self):
            return EXTRA_SERVICE_DESCRIPTION[self]

        def for_button(self, text: str) -> tuple[str, IntEnum]:
            return (text, self)

    class Factor(IntEnum):
        UNKNOWN = auto()
        DIFFICULT_ACCESS_TO_UNITS = auto()
        NO_ACCESS_TO_OBJECT = auto()
        CUSTOM_SIZES = auto()
        DAY_OFF_WORK = auto()
        WORKING_IN_ANOTHER_EMIRATE = auto()

        def __str__(self) -> str:
            return FACTOR_NAME[self]

        def get_descripiton(self):
            return FACTOR_DESCRIPTION[self]

        def for_button(self, text: str) -> tuple[str, IntEnum]:
            return (text, self)

    date: datetime = datetime.now()
    client: Client = Client()
    service: Service = Service.UNKNOWN
    description: str = ""
    extra_services: list[ExtraService] = field(default_factory=list)
    other_extra_services: list[str] = field(default_factory=list)
    work_factors: list[Factor] = field(default_factory=list)

    rooms: list[Room] = field(default_factory=list)

    def __post_init__(self):
        self.add_room()

    def add_room(self):
        self.rooms.append(Room())

    def add_factor(self, factor: Factor) -> None:
        if factor in self.work_factors:
            return
        self.work_factors.append(factor)

    def pop_factor(self, factor: Factor) -> None:
        self.work_factors.remove(factor)

    def clear_extra_services(self) -> None:
        self.extra_services.clear()
        self.other_extra_services.clear()

    async def dict_with_binary(self, bot) -> dict:
        return {
            "Outline": {
                "date": self.date,
                "name": self.client.name,
                "phone_number": self.client.phone,
                "address": self.client.address,
                "description": self.service.get_description(),
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


SERVICE_NAMES = {
    Report.Service.UNKNOWN: "",
    Report.Service.PREMIUM: "Premium",
    Report.Service.PREMIUM_EXTRA: "Premium + Extra",
    Report.Service.OTHER_REPAIR_SERVICES: "Other Repair Services",
}

SERVICE_DESCRIPTION = {
    Report.Service.PREMIUM: "This included supply/return grills cleaning (out-of-place) and sanitation, air supply/return duct vacuum and air-brush cleaning, duct sanitation (anti-germ and fungicide), air filters wash-throug and polyester filter installation.",
    Report.Service.PREMIUM_EXTRA: "This included supply/return grills cleaning (out-of-place) and sanitation, air supply/return duct vacuum and air-brush cleaning, duct sanitation (anti-germ and fungicide), air filters wash-throug and polyester filter installation.",
    Report.Service.OTHER_REPAIR_SERVICES: "Minor repairs around the house, not related to the repair of air conditioners and ventilation",
}

EXTRA_SERVICE_NAME = {
    Report.ExtraService.UNKNOWN: "",
    Report.ExtraService.THERMAIL_INSULATOR_CHANGE_JOB: "Thermal insulator change job",
    Report.ExtraService.NEW_POLYESTER_FILTERS_INSTALLATION: "New polyester filters installation",
    Report.ExtraService.COLD_FOG_MACHINE_DISINFECTIONS: "Cold fog machine disinfections",
    Report.ExtraService.REPAIR_WORKS: "Repair Works",
}

EXTRA_SERVICE_DESCRIPTION = {
    Report.ExtraService.UNKNOWN: "",
    Report.ExtraService.THERMAIL_INSULATOR_CHANGE_JOB: "Thermal insulator change job",
    Report.ExtraService.NEW_POLYESTER_FILTERS_INSTALLATION: "fog machine sanitation with OxyPro 7.5 All Purpose Disinfectant Activated Stabilised Hydrogen Peroxide Concentrate",
    Report.ExtraService.COLD_FOG_MACHINE_DISINFECTIONS: "polyester or other recommended by us type of air filter installation/change/wash-through",
    Report.ExtraService.REPAIR_WORKS: "minor repair and maintenance works as described in detail in the invoice",
}

FACTOR_NAME = {
    Report.Factor.DIFFICULT_ACCESS_TO_UNITS: "Cumbersome and difficult access",
    Report.Factor.NO_ACCESS_TO_OBJECT: "NO_ACCESS_TO_OBJECT",
    Report.Factor.CUSTOM_SIZES: "CUSTOM_SIZES",
    Report.Factor.DAY_OFF_WORK: "DAY_OFF_WORK",
    Report.Factor.WORKING_IN_ANOTHER_EMIRATE: "WORKING_INT_ANOTHER_EMIRATE",
}

FACTOR_DESCRIPTION = {
    Report.Factor.DIFFICULT_ACCESS_TO_UNITS: "Cumbersome and otherwise difficult access to units (ceiling access panels located far from AC units, access panels being less than 60 cm and similar) which affected the overall time of works",
    Report.Factor.NO_ACCESS_TO_OBJECT: "Property access permit not applied for/provided/procured for by the Client in advance",
    Report.Factor.CUSTOM_SIZES: "Duct grills and/or diffusers are of the length more than 2 meters long and system has not been serviced for a long time",
    Report.Factor.DAY_OFF_WORK: "The works performed on a weekend or on a UAE National Holiday",
    Report.Factor.WORKING_IN_ANOTHER_EMIRATE: "The Client's premises are located outside Dubai, in other emirate",
}

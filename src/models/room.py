from aiogram import types

from dataclasses import dataclass, field

from enum import Enum, auto

from typing import BinaryIO


@dataclass
class Room:
    class Type(str, Enum):
        UNKNOWN = ""
        KITCHEN = "Kitchen"
        BEDROOM = "Bedroom"
        LIVING_ROOM = "Living_room"
        OTHER = "Other"

        def __str__(self) -> str:
            return str(self.value)

    type: Type = Type.UNKNOWN
    room_object: str = ""
    photo_before: BinaryIO | None = None
    photo_after: BinaryIO | None = None

    def dict(self) -> dict:
        return {
            "room": self.get_name(),
            "object": self.room_object,
            "img_before": self.photo_before,
            "img_after": self.photo_after,
        }

    def get_name(self) -> str:
        return str(self.type)

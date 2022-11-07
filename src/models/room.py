from aiogram import types

from dataclasses import dataclass, field

from enum import Enum, auto


@dataclass
class Room:
    class Type(str, Enum):
        UNKNOWN = ""
        KITCHEN = "Kitchen"
        BEDROOM = "Bedroom"
        LIVING_ROOM = "Living_room"
        OTHER = "Other"

    type: Type = Type.UNKNOWN
    photo_before: types.PhotoSize | None = None
    photo_after: types.PhotoSize | None = None

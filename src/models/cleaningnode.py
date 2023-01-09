from typing import BinaryIO
from aiogram import types, Bot

from dataclasses import dataclass, field

from enum import IntEnum


@dataclass
class CleaningNode:
    class Type(IntEnum):
        UNKNOWN = -1
        DEFAULT = 0
        OTHER = 1

    name: str
    type: Type
    photo_before: types.PhotoSize | None = None
    photo_after: types.PhotoSize | None = None

    def for_button(self, text: str) -> tuple[str, ...]:
        return (text, self)


DEFAULT_CLEANING_NODES = [
    CleaningNode("grills", type=CleaningNode.Type.DEFAULT),
    CleaningNode("duct", type=CleaningNode.Type.DEFAULT),
    CleaningNode("pan", type=CleaningNode.Type.DEFAULT),
    CleaningNode("radiator", type=CleaningNode.Type.DEFAULT),
    CleaningNode("filter", type=CleaningNode.Type.DEFAULT),
    CleaningNode("blades", type=CleaningNode.Type.DEFAULT),
]

from typing import BinaryIO
from aiogram import types, Bot
from aiogram.utils.i18n import lazy_gettext as __

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
    button_text: str = ""

    def __eq__(self, other):
        if other is None:
            return False
        return self.name == other.name and self.type == other.type

    def __post_init__(self):
        if self.button_text == "":
            self.button_text = self.name


DEFAULT_CLEANING_NODES = [
    CleaningNode("grills", type=CleaningNode.Type.DEFAULT),
    CleaningNode("duct", type=CleaningNode.Type.DEFAULT),
    CleaningNode("pan", type=CleaningNode.Type.DEFAULT),
    CleaningNode("radiator", type=CleaningNode.Type.DEFAULT),
    CleaningNode("filter", type=CleaningNode.Type.DEFAULT),
    CleaningNode("blades", type=CleaningNode.Type.DEFAULT),
    CleaningNode("ceiling area", type=CleaningNode.Type.DEFAULT),
]

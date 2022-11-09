from typing import BinaryIO
from aiogram import types, Bot

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

        def __str__(self) -> str:
            return str(self.value)

    type: Type = Type.UNKNOWN
    room_object: str = ""
    photo_before: types.PhotoSize | None = None
    photo_after: types.PhotoSize | None = None

    async def dict_with_binary(self, bot: Bot) -> dict:
        return {
            "room": self.get_name(),
            "object": self.room_object,
            "img_before": await download_image(bot, self.photo_before),
            "img_after": await download_image(bot, self.photo_after),
        }

    def get_name(self) -> str:
        return str(self.type)


async def download_image(bot: Bot, photo: types.PhotoSize | None) -> BinaryIO | None:
    if photo is None:
        raise ValueError("Photo is None")
    return await bot.download(photo.file_id)

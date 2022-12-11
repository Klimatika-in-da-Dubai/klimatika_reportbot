from typing import BinaryIO
from aiogram import types, Bot

from dataclasses import dataclass, field

from enum import Enum, auto


@dataclass
class Room:
    class Type(str, Enum):
        UNKNOWN = ""
        BEDROOM = "Bedroom"
        LIVING_ROOM = "Living Room"
        KITCHEN = "Kitchen"

        def __str__(self) -> str:
            return str(self.value)

        def for_button(self, text: str) -> tuple[str, ...]:
            return (text, self)

    room_type: Type = Type.UNKNOWN
    room_object: str = ""

    photo_before_vent: types.PhotoSize | None = None
    photo_before_duct: types.PhotoSize | None = None
    photo_before_pallet: types.PhotoSize | None = None
    photo_before_radiator: types.PhotoSize | None = None
    photo_before_filter: types.PhotoSize | None = None
    photo_before_impelers: types.PhotoSize | None = None

    photo_after_vent: types.PhotoSize | None = None
    photo_after_duct: types.PhotoSize | None = None
    photo_after_pallet: types.PhotoSize | None = None
    photo_after_radiator: types.PhotoSize | None = None
    photo_after_filter: types.PhotoSize | None = None
    photo_after_impelers: types.PhotoSize | None = None

    async def dict_with_binary(self, bot: Bot) -> dict:
        return {
            "room": self.room_type,
            "object": self.room_object,
            "grills": {
                "img_before": await download_image(bot, self.photo_before_vent),
                "img_after": await download_image(bot, self.photo_after_vent),
            },
            "duct": {
                "img_before": await download_image(bot, self.photo_before_duct),
                "img_after": await download_image(bot, self.photo_after_duct),
            },
            "pan": {
                "img_before": await download_image(bot, self.photo_before_pallet),
                "img_after": await download_image(bot, self.photo_after_pallet),
            },
            "radiator": {
                "img_before": await download_image(bot, self.photo_before_radiator),
                "img_after": await download_image(bot, self.photo_after_radiator),
            },
            "filter": {
                "img_before": await download_image(bot, self.photo_before_filter),
                "img_after": await download_image(bot, self.photo_after_filter),
            },
            "blades": {
                "img_before": await download_image(bot, self.photo_before_impelers),
                "img_after": await download_image(bot, self.photo_after_impelers),
            },
        }


async def download_image(bot: Bot, photo: types.PhotoSize | None) -> BinaryIO | None:
    if photo is None:
        raise ValueError("Photo is None")
    return await bot.download(photo.file_id)

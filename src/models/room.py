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

    photo_before_vent: list[types.PhotoSize] = field(default_factory=list)
    photo_before_duct: list[types.PhotoSize] = field(default_factory=list)
    photo_before_pallet: list[types.PhotoSize] = field(default_factory=list)
    photo_before_radiator: list[types.PhotoSize] = field(default_factory=list)
    photo_before_filter: list[types.PhotoSize] = field(default_factory=list)
    photo_before_impelers: list[types.PhotoSize] = field(default_factory=list)

    photo_after_vent: list[types.PhotoSize] = field(default_factory=list)
    photo_after_duct: list[types.PhotoSize] = field(default_factory=list)
    photo_after_pallet: list[types.PhotoSize] = field(default_factory=list)
    photo_after_radiator: list[types.PhotoSize] = field(default_factory=list)
    photo_after_filter: list[types.PhotoSize] = field(default_factory=list)
    photo_after_impelers: list[types.PhotoSize] = field(default_factory=list)

    async def dict_with_binary(self, bot: Bot) -> dict:
        return {
            "room": self.room_type,
            "object": self.room_object,
            "grills": {
                "img_before": await download_images(bot, self.photo_before_vent),
                "img_after": await download_images(bot, self.photo_after_vent),
            },
            "duct": {
                "img_before": await download_images(bot, self.photo_before_duct),
                "img_after": await download_images(bot, self.photo_after_duct),
            },
            "pan": {
                "img_before": await download_images(bot, self.photo_before_pallet),
                "img_after": await download_images(bot, self.photo_after_pallet),
            },
            "radiator": {
                "img_before": await download_images(bot, self.photo_before_radiator),
                "img_after": await download_images(bot, self.photo_after_radiator),
            },
            "filter": {
                "img_before": await download_images(bot, self.photo_before_filter),
                "img_after": await download_images(bot, self.photo_after_filter),
            },
            "blades": {
                "img_before": await download_images(bot, self.photo_before_impelers),
                "img_after": await download_images(bot, self.photo_after_impelers),
            },
        }


async def download_images(bot, photos: list[types.PhotoSize]) -> list[BinaryIO] | None:
    if len(photos) == 0:
        return
    return [await download_image(bot, image) for image in photos]


async def download_image(bot: Bot, photo: types.PhotoSize | None) -> BinaryIO | None:
    if photo is None:
        raise ValueError("Photo is None")
    return await bot.download(photo.file_id)

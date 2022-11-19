from aiogram import types
from datetime import datetime
import dateparser

from loader import users


from src.models.room import Room
from src.models.report import Report


def get_date(text: str | None) -> datetime:
    if text is None:
        return datetime.now()
    date = dateparser.parse(text, settings={"DATE_ORDER": "DMY"})
    if date is None:
        return datetime.now()
    return date


def get_name(text: str | None) -> str:
    if text is None:
        return ""
    return text


def get_email(text: str | None) -> str:
    if text is None:
        return ""
    return text


def get_phone(text: str | None) -> str:
    if text is None:
        return ""

    return text.replace(" ", "").replace("+", "").replace("-", "")


def get_address(text: str | None) -> str:
    if text is None:
        return ""
    return text


def get_rooms_count(text: str | None) -> int:
    if text is None:
        return 0
    return int(text)


def get_room_type(text: str | None) -> Room.Type:
    if text is None:
        return Room.Type.UNKNOWN

    return Room.Type(text)


def get_room_object(text: str | None) -> str:
    if text is None:
        return ""
    return text


def get_current_user_report(chat_id: int) -> Report:
    return users[chat_id]


def get_current_user_room(chat_id: int) -> Room:
    current_room_index = users[chat_id].room_index
    return users[chat_id].rooms[current_room_index]


def get_photo(photos: list[types.PhotoSize] | None) -> types.PhotoSize | None:
    if photos is None:
        return None
    photo = photos[-1]
    return photo

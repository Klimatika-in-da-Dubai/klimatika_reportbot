from aiogram import types

from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.misc.getters import get_current_user_report
from src.models.report import Report
from src.models.room import Room


def get_service_keyboard(
    chat_id: int, services: list[tuple[str, Report.Service]]
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for service in services:
        builder.add(
            types.InlineKeyboardButton(text=service[0], callback_data=service[1])
        )
    builder.adjust(1)
    return builder.as_markup()


def get_yes_no_keyboard(chat_id: int, yes: str, no: str) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text=yes, callback_data="yes"))
    builder.add(types.InlineKeyboardButton(text=no, callback_data="no"))
    return builder.as_markup()


def get_extra_service_keyboard(
    chat_id: int, extra_services: list[tuple[str, Report.ExtraService]], enter: str
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    report = get_current_user_report(chat_id)

    for extra_service in extra_services:
        status = "✅" if extra_service[1] in report.extra_services else "❌"
        builder.add(
            types.InlineKeyboardButton(
                text=f"{extra_service[0]} {status}", callback_data=extra_service[1]
            )
        )
    builder.add(types.InlineKeyboardButton(text=enter, callback_data="enter"))

    builder.adjust(1)
    return builder.as_markup()


def get_room_type_keyboard(
    chat_id: int, room_types: list[tuple[str, Room.Type]]
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for room_type in room_types:
        builder.add(
            types.InlineKeyboardButton(text=room_type[0], callback_data=room_type[1])
        )
    builder.adjust(1)
    return builder.as_markup()

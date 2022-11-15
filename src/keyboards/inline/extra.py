from aiogram import types

from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.misc.getters import get_current_user_report
from src.models.report import Report


def get_extra_service_keyboard(
    chat_id: int, extra_services: list, enter: str
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    report = get_current_user_report(chat_id)

    for extra_service in extra_services:
        service = Report.ExtraService(extra_service)
        status = "✅" if service in report.extra_services else "❌"
        builder.add(
            types.InlineKeyboardButton(
                text=f"{service} {status}", callback_data=service
            )
        )
    builder.add(types.InlineKeyboardButton(text=enter, callback_data="enter"))

    builder.adjust(1)
    return builder.as_markup()

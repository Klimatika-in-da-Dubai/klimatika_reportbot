from aiogram import types

from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.misc.getters import get_current_user_report


def get_extra_service_keyboard(
    chat_id: int, extra_services: list
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    report = get_current_user_report(chat_id)

    for service in extra_services:
        status = "✅" if service in report.extra_services else "❌"
        builder.add(
            types.InlineKeyboardButton(
                text=f"{service} {status}", callback_data=service
            )
        )

    builder.adjust(1)
    return builder.as_markup()

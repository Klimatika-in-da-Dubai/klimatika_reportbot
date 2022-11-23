from aiogram import types

from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.misc.getters import get_current_user_report
from src.models import Room, Report, Client
from src.callbackdata import ExtraServiceCB, ServiceCB, OtherExtraServiceCB, ClientCB



def get_client_type_keyboard(
    chat_id: int, client_types: list[tuple[str, Client.Type]]
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for text, client_type in client_types:
        builder.add(
            types.InlineKeyboardButton(
                text=text, callback_data=ClientCB(type=client_type).pack()
            )
        )
    builder.adjust(1)
    return builder.as_markup()


def get_service_keyboard(
    chat_id: int, services: list[tuple[str, Report.Service]]
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for text, service in services:
        builder.add(
            types.InlineKeyboardButton(
                text=text,
                callback_data=ServiceCB(service=service).pack(),
            )
        )
    builder.adjust(1)
    return builder.as_markup()


def get_extra_service_keyboard(
    chat_id: int,
    extra_services: list[tuple[str, Report.ExtraService]],
    other: str,
    enter: str,
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    report = get_current_user_report(chat_id)

    for text, extra_service in extra_services:
        status = "✅" if extra_service in report.extra_services else "❌"
        builder.add(
            types.InlineKeyboardButton(
                text=f"{text} {status}",
                callback_data=ExtraServiceCB(action="", service=extra_service).pack(),
            )
        )
    builder.add(
        types.InlineKeyboardButton(
            text=other + "➕",
            callback_data=OtherExtraServiceCB(action="add", id=-1).pack(),
        )
    )
    for id, extra_service in enumerate(report.other_extra_services):
        builder.add(
            types.InlineKeyboardButton(
                text=extra_service,
                callback_data=OtherExtraServiceCB(action="delete", id=id).pack(),
            )
        )

    builder.add(
        types.InlineKeyboardButton(
            text=enter,
            callback_data=ExtraServiceCB(
                action="enter", service=Report.ExtraService.UNKNOWN
            ).pack(),
        )
    )

    builder.adjust(1)
    return builder.as_markup()


def get_yes_no_keyboard(chat_id: int, yes: str, no: str) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text=yes, callback_data="yes"))
    builder.add(types.InlineKeyboardButton(text=no, callback_data="no"))
    return builder.as_markup()



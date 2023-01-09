from aiogram import types

from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.misc.getters import get_current_user_report, get_current_user_room
from src.models import Room, Report, Client, CleaningNode
from src.callbackdata import (
    ExtraServiceCB,
    ServiceCB,
    OtherExtraServiceCB,
    ClientCB,
    RoomTypeCB,
    CleaningNodeCB,
)


def get_room_type_keyboard(
    chat_id: int, room_types: list[tuple[str, Room.Type]]
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for text, room_type in room_types:
        builder.add(
            types.InlineKeyboardButton(
                text=text, callback_data=RoomTypeCB(type=room_type).pack()
            )
        )
    builder.adjust(1)
    return builder.as_markup()


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
    for id, extra_service in enumerate(report.other_extra_services):
        builder.add(
            types.InlineKeyboardButton(
                text=extra_service,
                callback_data=OtherExtraServiceCB(action="delete", id=id).pack(),
            )
        )

    builder.add(
        types.InlineKeyboardButton(
            text=other + "➕",
            callback_data=OtherExtraServiceCB(action="add", id=-1).pack(),
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


def get_cleaning_node_keyboard(
    chat_id: int,
    cleaning_nodes: list[tuple[str, CleaningNode]],
    other: str,
    enter: str,
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    room = get_current_user_room(chat_id)
    for text, cleaning_node in cleaning_nodes:
        status = [cleaning_node, True] in room.default_cleaning_nodes
        status_text = "✅" if status else "❌"
        callback_data = CleaningNodeCB(
            action="delete" if status else "add",
            name=cleaning_node.name,
            type=cleaning_node.type,
        )
        builder.add(
            types.InlineKeyboardButton(
                text=f"{text} {status_text}",
                callback_data=callback_data.pack(),
            )
        )

    for cleaning_node in room.cleaning_nodes:
        if cleaning_node in cleaning_nodes:
            continue
        callback_data = CleaningNodeCB(
            action="delete",
            name=cleaning_node.name,
            type=cleaning_node.type,
        )
        builder.add(
            types.InlineKeyboardButton(
                text=f"{cleaning_node.name}",
                callback_data=callback_data.pack(),
            )
        )

    builder.add(
        types.InlineKeyboardButton(
            text=other + "➕",
            callback_data=CleaningNodeCB(
                action="add_other", name="", type=CleaningNode.Type.UNKNOWN
            ).pack(),
        )
    )

    builder.add(
        types.InlineKeyboardButton(
            text=enter,
            callback_data=CleaningNodeCB(
                action="enter", name="", type=CleaningNode.Type.UNKNOWN
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

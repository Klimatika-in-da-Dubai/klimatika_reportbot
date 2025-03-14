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
    FactorCB,
)


def get_room_type_keyboard(
    chat_id: int, room_types: list[tuple[str, Room.Type]], other: str,
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for text, room_type in room_types:
        builder.add(
            types.InlineKeyboardButton(
                text=text, callback_data=RoomTypeCB(type=room_type).pack()
            )
        )
    
    builder.add(
        types.InlineKeyboardButton(
            text=other + "➕",
            callback_data=RoomTypeCB(
                action="other_room",
                index=-1,
                type=Room.Type.UNKNOWN,
            ).pack(),
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

    # builder.add(
    #     types.InlineKeyboardButton(
    #         text=other + "➕",
    #         callback_data=OtherExtraServiceCB(action="add", id=-1).pack(),
    #     )
    # )

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
    cleaning_nodes: list[CleaningNode],
    other: str,
    enter: str,
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    room = get_current_user_room(chat_id)
    for index, cleaning_node in enumerate(cleaning_nodes):
        status = [cleaning_node, True] in room.default_cleaning_nodes
        status_text = "✅" if status else "❌"
        callback_data = CleaningNodeCB(
            action="delete" if status else "add",
            index=index,
            type=cleaning_node.type,
        )
        builder.add(
            types.InlineKeyboardButton(
                text=f"{cleaning_node.button_text} {status_text}",
                callback_data=callback_data.pack(),
            )
        )

    for index, cleaning_node in enumerate(room.cleaning_nodes):
        if cleaning_node in cleaning_nodes:
            continue
        callback_data = CleaningNodeCB(
            action="delete",
            index=index,
            type=cleaning_node.type,
        )
        builder.add(
            types.InlineKeyboardButton(
                text=f"{cleaning_node.button_text}",
                callback_data=callback_data.pack(),
            )
        )

    builder.add(
        types.InlineKeyboardButton(
            text=other + "➕",
            callback_data=CleaningNodeCB(
                action="add_other",
                index=-1,
                type=CleaningNode.Type.UNKNOWN,
            ).pack(),
        )
    )

    builder.add(
        types.InlineKeyboardButton(
            text=enter,
            callback_data=CleaningNodeCB(
                action="enter", index=-1, type=CleaningNode.Type.UNKNOWN
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


def get_factors_keyboard(
    chat_id: int, factors: list[tuple[str, Report.Factor]], enter: str
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    report = get_current_user_report(chat_id)
    for i, (factor_button_text, factor) in enumerate(factors):
        status = factor in report.work_factors
        status_text = "✅" if status else "❌"
        action = "delete" if status else "add"
        callback_data = FactorCB(action=action, factor=factor, index=i).pack()
        builder.add(
            types.InlineKeyboardButton(
                text=f"{factor_button_text} {status_text}", callback_data=callback_data
            )
        )

    builder.add(
        types.InlineKeyboardButton(
            text=f"{enter}",
            callback_data=FactorCB(
                action="enter", factor=Report.Factor.UNKNOWN, index=-1
            ).pack(),
        )
    )
    builder.adjust(1)
    return builder.as_markup()



# Функция для создания клавиатуры с кнопкой "Пропустить"
def get_skip_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text=("Skip"), callback_data="skip"))
    return builder.as_markup()
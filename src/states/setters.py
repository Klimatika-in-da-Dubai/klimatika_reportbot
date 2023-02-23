from aiogram import types
from aiogram.fsm.context import FSMContext

from aiogram.utils.i18n import gettext as _

from src.states import Form
from src.keyboards import inline
from src.misc import getters as get

from src.models import Report, CleaningNode


async def set_client_name_state(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.client_name)
    await message.answer(_("Enter clients Name"))


async def set_date_state(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.date)
    await message.answer(
        _(
            "Enter date of visit in format DAY MONTH YEAR.\n\nFor example: 1 12 2022 (December the 1st, 2022)"
        )
    )


async def set_client_phone_state(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.client_phone)
    await message.answer(_("Enter Phone number"))


async def set_client_address_state(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.client_address)
    await message.answer(_("Enter client address:"))


async def set_service_state(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.service)
    await inline.send_service_keyboard(message)


async def set_extra_service_state(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.extra_service)
    await inline.send_extra_service_keyboard(message)


async def set_state_work_factors(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.work_factors)
    await inline.send_factors_keyboard(message)


async def set_room_cleaning_nodes_state(
    message: types.Message, state: FSMContext
) -> None:
    await state.set_state(Form.room_cleaning_nodes)
    await inline.send_cleaning_node_keyboard(message)


async def set_state_room_cleaning_nodes(message: types.Message, state: FSMContext):
    report = get.get_current_user_report(message.chat.id)
    if report.service != Report.Service.OTHER_REPAIR_SERVICES:
        set_default_cleaning_nodes(message)
    await state.set_state(Form.room_cleaning_nodes)
    await inline.send_cleaning_node_keyboard(message)


def set_default_cleaning_nodes(message: types.Message):
    DEFAULT_CLEANING_NODES = [
        CleaningNode("grills", button_text=_("grills"), type=CleaningNode.Type.DEFAULT),
        CleaningNode("duct", button_text=_("duct"), type=CleaningNode.Type.DEFAULT),
        CleaningNode("pan", button_text=_("pan"), type=CleaningNode.Type.DEFAULT),
        CleaningNode(
            "radiator",
            button_text=_("radiator"),
            type=CleaningNode.Type.DEFAULT,
        ),
        CleaningNode("filter", button_text=_("filter"), type=CleaningNode.Type.DEFAULT),
        CleaningNode("blades", button_text=_("blades"), type=CleaningNode.Type.DEFAULT),
    ]
    room = get.get_current_user_room(message.chat.id)
    for node in DEFAULT_CLEANING_NODES:
        room.set_default_node(node)


async def set_img_before_state(message: types.Message, state: FSMContext) -> None:
    room = get.get_current_user_room(message.chat.id)
    await state.set_state(Form.cleaning_node_img_before)
    await message.answer(
        _("Send photo BEFORE for") + " " + room.current_node.button_text
    )


async def set_img_after_state(message: types.Message, state: FSMContext) -> None:
    room = get.get_current_user_room(message.chat.id)
    await state.set_state(Form.cleaning_node_img_after)
    await message.answer(
        _("Send photo AFTER for") + " " + room.current_node.button_text
    )


async def set_add_room_state(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.add_room)
    await inline.send_yes_no_keboard(message, _("Do you want to add room?"))

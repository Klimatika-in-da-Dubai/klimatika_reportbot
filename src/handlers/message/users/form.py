from aiogram import Router, types, F
from aiogram.utils.i18n import gettext as _

from aiogram.fsm.context import FSMContext

import src.keyboards.inline as inline


from src.states.form import Form
from src.models import Report, Room, Client, CleaningNode
import src.misc.validators as vld
import src.misc.getters as get
from src.states import setters as set_state


form_router = Router()


@form_router.message(Form.client_name, F.text)
async def process_name(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_name(message.text):
        await message.answer(_("Incorrect Name"))
        return

    name = get.get_name(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.client.name = name
    await set_state.set_date_state(message, state)


@form_router.message(Form.date, F.text)
async def process_date(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_date(message.text):
        await message.answer(_("Incorrect Date"))
        return

    date = get.get_date(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.date = date
    await set_state.set_client_phone_state(message, state)


@form_router.message(Form.client_phone, F.text)
async def process_phone(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_phone(message.text):
        await message.answer(_("Incorrect phone"))
        return

    phone = get.get_phone(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.client.phone = phone
    await set_state.set_client_address_state(message, state)


@form_router.message(Form.client_address, F.text)
async def process_address(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_address(message.text):
        await message.answer(_("Incorrect address"))
        return

    address = get.get_address(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.client.address = address
    await set_state.set_service_state(message, state)


@form_router.message(Form.extra_service_await_answer, F.text)
async def process_extra_service_add_other(message: types.Message, state: FSMContext):
    report = get.get_current_user_report(message.chat.id)
    report.other_extra_services.append(message.text)
    await set_state.set_extra_service_state(message, state)


@form_router.message(Form.cleaning_node_await_answer, F.text)
async def process_cleaning_node_add_other(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    if len(message.text) > 31:
        await message.answer(_("Cleaning node name is too long! Should be < 31"))
        return
    room.add_node(CleaningNode(message.text, CleaningNode.Type.OTHER))
    await set_state.set_room_cleaning_nodes_state(message, state)


@form_router.message(Form.cleaning_node_img_before, F.photo)
async def process_cleaning_node_img_before(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.current_node.photo_before = get.get_photo(message.photo)
    room.next_cleaning_node()

    if room.nodes_queue_empty():
        room.create_nodes_queue()
        await set_state.set_img_after_state(message, state)
        return

    await message.answer(
        _("Send photo BEFORE for") + " " + room.current_node.button_text
    )


@form_router.message(Form.cleaning_node_img_after, F.photo)
async def process_cleaning_node_img_after(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.current_node.photo_after = get.get_photo(message.photo)
    room.next_cleaning_node()

    if room.nodes_queue_empty():
        await set_state.set_add_room_state(message, state)
        return

    await message.answer(
        _("Send photo AFTER for") + " " + room.current_node.button_text
    )

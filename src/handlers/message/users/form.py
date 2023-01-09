from aiogram import Router, types, F
from aiogram.utils.i18n import gettext as _

from aiogram.fsm.context import FSMContext

import src.keyboards.inline as inline


from src.states.form import Form
from src.models import Report, Room, Client, CleaningNode
import src.misc.validators as vld
import src.misc.getters as get


form_router = Router()


@form_router.message(Form.client_name, F.text)
async def process_name(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_name(message.text):
        await message.answer(_("Incorrect Name"))
        return

    name = get.get_name(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.client.name = name
    await state.set_state(Form.date)
    await message.answer(
        _(
            "Enter date of visit in format DAY MONTH YEAR.\n\nFor example: 1 12 2022 (December the 1st, 2022)"
        )
    )


@form_router.message(Form.date, F.text)
async def process_date(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_date(message.text):
        await message.answer(_("Incorrect Date"))
        return

    date = get.get_date(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.date = date
    await state.set_state(Form.client_phone)
    await message.answer(_("Enter Phone number"))


@form_router.message(Form.client_phone, F.text)
async def process_phone(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_phone(message.text):
        await message.answer(_("Incorrect phone"))
        return

    phone = get.get_phone(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.client.phone = phone
    await state.set_state(Form.client_address)
    await message.answer(_("Enter client address:"))


@form_router.message(Form.client_address, F.text)
async def process_address(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_address(message.text):
        await message.answer(_("Incorrect address"))
        return

    address = get.get_address(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.client.address = address
    await state.set_state(Form.service)
    await inline.send_service_keyboard(message)


@form_router.message(Form.extra_service_await_answer, F.text)
async def process_extra_service_add_other(message: types.Message, state: FSMContext):
    report = get.get_current_user_report(message.chat.id)
    report.other_extra_services.append(message.text)
    await state.set_state(Form.extra_service)
    await inline.send_extra_service_keyboard(message)


@form_router.message(Form.cleaning_node_await_answer, F.text)
async def process_cleaning_node_add_other(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.add_node(CleaningNode(message.text, CleaningNode.Type.OTHER))
    await state.set_state(Form.room_cleaning_nodes)
    await inline.send_cleaning_node_keyboard(message)

from aiogram import Router, types, F
from aiogram.utils.i18n import gettext as _

from aiogram.fsm.context import FSMContext

import src.keyboards.inline as inline


from src.states.form import Form
from src.models import Report, Room, Client
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


@form_router.message(Form.room_before_vent, F.photo)
async def process_room_before_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_before_vent.append(get.get_photo(message.photo))
    if len(room.photo_before_vent) > 1:
        return
    await state.set_state(Form.room_before_duct)
    await message.answer(_("Send photo BEFORE works for duct"))


@form_router.message(Form.room_before_duct, F.photo)
async def process_room_before_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_before_duct.append(get.get_photo(message.photo))
    if len(room.photo_before_duct) > 1:
        return
    await state.set_state(Form.room_before_pallet)
    await message.answer(_("Send photo BEFORE works for pan"))


@form_router.message(Form.room_before_pallet, F.photo)
async def process_room_before_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_before_pallet.append(get.get_photo(message.photo))
    if len(room.photo_before_pallet) > 1:
        return
    await state.set_state(Form.room_before_radiator)
    await message.answer(_("Send photo BEFORE works for radiator"))


@form_router.message(Form.room_before_radiator, F.photo)
async def process_room_before_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_before_radiator.append(get.get_photo(message.photo))
    if len(room.photo_before_radiator) > 1:
        return
    await state.set_state(Form.room_before_filter)
    await message.answer(_("Send photo BEFORE works for filter"))


@form_router.message(Form.room_before_filter, F.photo)
async def process_room_before_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_before_filter.append(get.get_photo(message.photo))
    if len(room.photo_before_filter) > 1:
        return
    await state.set_state(Form.room_before_impelers)
    await message.answer(_("Send photo BEFORE works for blades"))


@form_router.message(Form.room_before_impelers, F.photo)
async def process_room_before_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_before_impelers.append(get.get_photo(message.photo))
    if len(room.photo_before_impelers) > 1:
        return
    await state.set_state(Form.room_after_vent)
    await message.answer(_("Send photo AFTER works for grills"))


#####
@form_router.message(Form.room_after_vent, F.photo)
async def process_room_after_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_after_vent.append(get.get_photo(message.photo))
    if len(room.photo_after_vent) > 1:
        return
    await state.set_state(Form.room_after_duct)
    await message.answer(_("Send photo AFTER works for duct"))


@form_router.message(Form.room_after_duct, F.photo)
async def process_room_after_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_after_duct.append(get.get_photo(message.photo))
    if len(room.photo_after_duct) > 1:
        return
    await state.set_state(Form.room_after_pallet)
    await message.answer(_("Send photo AFTER works for pan"))


@form_router.message(Form.room_after_pallet, F.photo)
async def process_room_after_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_after_pallet.append(get.get_photo(message.photo))
    if len(room.photo_after_pallet) > 1:
        return
    await state.set_state(Form.room_after_radiator)
    await message.answer(_("Send photo AFTER works for radiator"))


@form_router.message(Form.room_after_radiator, F.photo)
async def process_room_after_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_after_radiator.append(get.get_photo(message.photo))
    if len(room.photo_after_radiator) > 1:
        return
    await state.set_state(Form.room_after_filter)
    await message.answer(_("Send photo AFTER works for filter"))


@form_router.message(Form.room_after_filter, F.photo)
async def process_room_after_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_after_filter.append(get.get_photo(message.photo))
    if len(room.photo_after_filter) > 1:
        return
    await state.set_state(Form.room_after_impelers)
    await message.answer(_("Send photo AFTER works for blades"))


@form_router.message(Form.room_after_impelers, F.photo)
async def process_room_after_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_after_impelers.append(get.get_photo(message.photo))
    if len(room.photo_after_impelers) > 1:
        return
    await state.set_state(Form.add_room)
    await inline.send_yes_no_keboard(message, _("Do you want to add room?"))

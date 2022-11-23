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
    await message.answer(_("Enter date of visit in format DAY MONTH YEAR"))


@form_router.message(Form.date, F.text)
async def process_date(message: types.Message, state: FSMContext) -> None:
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
    await state.set_state(Form.client_type)
    await inline.send_client_type_keyboard(message)


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


@form_router.message(Form.room_object, F.text)
async def process_room_object(message: types.Message, state: FSMContext):
    if not vld.is_valid_room_object(message.text):
        return

    object = get.get_room_object(message.text)
    room = get.get_current_user_room(message.chat.id)
    room.room_object = object
    await state.set_state(Form.room_before_vent)
    await message.answer(_("Send photo BEFORE works for vent"))


@form_router.message(Form.room_before_vent, F.photo)
async def process_room_before_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_before_vent = get.get_photo(message.photo)
    await state.set_state(Form.room_before_duct)
    await message.answer(_("Send photo BEFORE works for duct"))


@form_router.message(Form.room_before_duct, F.photo)
async def process_room_before_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_before_duct = get.get_photo(message.photo)
    await state.set_state(Form.room_before_pallet)
    await message.answer(_("Send photo BEFORE works for pallet"))


@form_router.message(Form.room_before_pallet, F.photo)
async def process_room_before_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_before_pallet = get.get_photo(message.photo)
    await state.set_state(Form.room_before_radiator)
    await message.answer(_("Send photo BEFORE works for radiator"))


@form_router.message(Form.room_before_radiator, F.photo)
async def process_room_before_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_before_radiator = get.get_photo(message.photo)
    await state.set_state(Form.room_before_filter)
    await message.answer(_("Send photo BEFORE works for filter"))


@form_router.message(Form.room_before_filter, F.photo)
async def process_room_before_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_before_filter = get.get_photo(message.photo)
    await state.set_state(Form.room_before_impelers)
    await message.answer(_("Send photo BEFORE works for impelers"))


@form_router.message(Form.room_before_impelers, F.photo)
async def process_room_before_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_before_impelers = get.get_photo(message.photo)
    await state.set_state(Form.room_after_vent)
    await message.answer(_("Send photo AFTER works for vent"))


#####
@form_router.message(Form.room_after_vent, F.photo)
async def process_room_after_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_after_vent = get.get_photo(message.photo)
    await state.set_state(Form.room_after_duct)
    await message.answer(_("Send photo AFTER works for duct"))


@form_router.message(Form.room_after_duct, F.photo)
async def process_room_after_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_after_duct = get.get_photo(message.photo)
    await state.set_state(Form.room_after_pallet)
    await message.answer(_("Send photo AFTER works for pallet"))


@form_router.message(Form.room_after_pallet, F.photo)
async def process_room_after_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_after_pallet = get.get_photo(message.photo)
    await state.set_state(Form.room_after_radiator)
    await message.answer(_("Send photo AFTER works for radiator"))


@form_router.message(Form.room_after_radiator, F.photo)
async def process_room_after_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_after_radiator = get.get_photo(message.photo)
    await state.set_state(Form.room_after_filter)
    await message.answer(_("Send photo AFTER works for filter"))


@form_router.message(Form.room_after_filter, F.photo)
async def process_room_after_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_after_filter = get.get_photo(message.photo)
    await state.set_state(Form.room_after_impelers)
    await message.answer(_("Send photo AFTER works for impelers"))


@form_router.message(Form.room_after_impelers, F.photo)
async def process_room_after_vent(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.photo_after_impelers = get.get_photo(message.photo)
    await state.set_state(Form.add_room)
    await inline.send_yes_no_keboard(message, _("Do you want to add room?"))

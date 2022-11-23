from aiogram import Router, types, F
from aiogram.utils.i18n import gettext as _

from aiogram.fsm.context import FSMContext

import src.keyboards.inline as inline


from src.states.form import Form
from src.models import Report, Room
import src.misc.validators as vld

import src.misc.getters as get


from loader import users

form_router = Router()


@form_router.message(Form.date, F.text)
async def process_date(message: types.Message, state: FSMContext) -> None:
    date = get.get_date(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.date = date
    await state.set_state(Form.name)
    await message.answer(_("Enter clients Name"))


@form_router.message(Form.name, F.text)
async def process_name(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_name(message.text):
        await message.answer(_("Incorrect Name"))
        return

    name = get.get_name(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.client.name = name
    await state.set_state(Form.phone)
    await message.answer(_("Enter Phone number"))


@form_router.message(Form.phone, F.text)
async def process_phone(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_phone(message.text):
        await message.answer(_("Incorrect phone"))
        return

    phone = get.get_phone(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.client.phone = phone
    await state.set_state(Form.email)
    await message.answer(_("Enter Email:"))


@form_router.message(Form.email, F.text)
async def process_email(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_email(message.text):
        await message.answer(_("Incorrect email"))
        return

    email = get.get_email(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.client.email = email
    await state.set_state(Form.address)
    await message.answer(_("Enter client address:"))


@form_router.message(Form.address, F.text)
async def process_address(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_address(message.text):
        await message.answer(_("Incorrect address"))
        return

    address = get.get_address(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.client.address = address
    await state.set_state(Form.service)
    await message.answer(
        _("Choose service:"),
        reply_markup=inline.get_service_keyboard(
            message.chat.id,
            [
                Report.Service.FULL.for_button(_("Full Cleaning")),
                Report.Service.BASE.for_button(_("Basic Cleaning")),
                Report.Service.WITHOUT_CLEANING.for_button(_("Wthout Cleaning")),
            ],
        ),
    )


@form_router.message(Form.rooms_count)
async def process_rooms_count(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_rooms_count(message.text):
        await message.answer(_("Incorrect rooms count"))
        return

    report = get.get_current_user_report(message.chat.id)
    rooms_count = get.get_rooms_count(message.text)
    report.rooms_count = rooms_count
    report.rooms = [Room() for _ in range(rooms_count)]
    await state.set_state(Form.room_type)
    await message.answer(
        _("Type of the {index} room").format(index=report.room_index + 1),
        reply_markup=inline.get_room_type_keyboard(
            message.chat.id,
            [
                Room.Type.KITCHEN.for_button(_("Kitchen")),
                Room.Type.BEDROOM.for_button(_("Bedroom")),
                Room.Type.LIVING_ROOM.for_button(_("Living Room")),
            ],
        ),
    )


@form_router.message(Form.room_object, F.text)
async def process_rooms_object(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_room_object(message.text):
        await message.answer(_("Incorrect comment"))
        return

    room_object = get.get_room_object(message.text)
    room = get.get_current_user_room(message.chat.id)
    room.room_object = room_object
    await state.set_state(Form.room_before)
    await message.answer(_("Send photo before works"))


@form_router.message(Form.room_before, F.photo)
async def process_room_before(message: types.Message, state: FSMContext) -> None:
    room = get.get_current_user_room(message.chat.id)
    room.photo_before = get.get_photo(message.photo)
    await state.set_state(Form.room_after)
    await message.answer(_("Send photo after works"))


@form_router.message(Form.room_after, F.photo)
async def process_room_after(message: types.Message, state: FSMContext) -> None:
    report = get.get_current_user_report(message.chat.id)
    room = get.get_current_user_room(message.chat.id)
    room.photo_after = get.get_photo(message.photo)
    if report.room_index + 1 < report.rooms_count:
        report.room_index += 1
        await state.set_state(Form.room_type)
        await message.answer(
            _("Type of the {index} room").format(index=report.room_index + 1),
            reply_markup=inline.get_room_type_keyboard(
                message.chat.id,
                [
                    Room.Type.KITCHEN.for_button(_("Kitchen")),
                    Room.Type.BEDROOM.for_button(_("Bedroom")),
                    Room.Type.LIVING_ROOM.for_button(_("Living Room")),
                ],
            ),
        )

        return

    await state.set_state(Form.extra)
    await message.answer(
        _("Do you want to add something?"),
        reply_markup=inline.get_yes_no_keyboard(
            message.chat.id, yes=_("Yes"), no=_("No")
        ),
    )

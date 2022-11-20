from aiogram import Router, types, F


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
    await message.answer("Enter clients Name")


@form_router.message(Form.name, F.text)
async def process_name(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_name(message.text):
        await message.answer("Incorrect Name")
        return

    name = get.get_name(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.name = name
    await state.set_state(Form.phone)
    await message.answer("Enter Phone number")


@form_router.message(Form.phone, F.text)
async def process_phone(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_phone(message.text):
        await message.answer("Incorrect phone")
        return

    phone = get.get_phone(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.phone = phone
    await state.set_state(Form.email)
    await message.answer("Enter Email:")


@form_router.message(Form.email, F.text)
async def process_email(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_email(message.text):
        await message.answer("Incorrect email")
        return

    email = get.get_email(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.email = email
    await state.set_state(Form.address)
    await message.answer("Enter client address:")


@form_router.message(Form.address, F.text)
async def process_address(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_address(message.text):
        await message.answer("Incorrect address")
        return

    address = get.get_address(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.address = address
    await state.set_state(Form.service)
    await message.answer(
        "Choose service:",
        reply_markup=inline.get_service_keyboard(
            message.chat.id,
            [
                (str(Report.service.FULL), Report.Service.FULL),
                (str(Report.Service.BASE), Report.Service.BASE),
                (str(Report.Service.WITHOUT_CLEANING), Report.Service.WITHOUT_CLEANING),
            ],
        ),
    )


@form_router.message(Form.rooms_count)
async def process_rooms_count(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_rooms_count(message.text):
        await message.answer("Incorrect rooms count")
        return

    report = get.get_current_user_report(message.chat.id)
    rooms_count = get.get_rooms_count(message.text)
    report.rooms_count = rooms_count
    report.rooms = [Room() for _ in range(rooms_count)]
    await state.set_state(Form.room_type)
    await message.answer(
        f"Type of the {users[message.chat.id].room_index + 1} room",
        reply_markup=inline.get_room_type_keyboard(
            message.chat.id,
            [
                (str(Room.Type.KITCHEN), Room.Type.KITCHEN),
                (str(Room.Type.BEDROOM), Room.Type.BEDROOM),
                (str(Room.Type.LIVING_ROOM), Room.Type.LIVING_ROOM),
            ],
        ),
    )


@form_router.message(Form.room_object, F.text)
async def process_rooms_object(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_room_object(message.text):
        await message.answer("Incorrect comment")
        return

    room_object = get.get_room_object(message.text)
    room = get.get_current_user_room(message.chat.id)
    room.room_object = room_object
    await state.set_state(Form.room_before)
    await message.answer("Send photo before works")


@form_router.message(Form.room_before, F.photo)
async def process_room_before(message: types.Message, state: FSMContext) -> None:
    room = get.get_current_user_room(message.chat.id)
    room.photo_before = get.get_photo(message.photo)
    await state.set_state(Form.room_after)
    await message.answer(f"Send photo after works")


@form_router.message(Form.room_after, F.photo)
async def process_room_after(message: types.Message, state: FSMContext) -> None:
    report = get.get_current_user_report(message.chat.id)
    room = get.get_current_user_room(message.chat.id)
    room.photo_after = get.get_photo(message.photo)
    if report.room_index + 1 < users[message.chat.id].rooms_count:
        users[message.chat.id].room_index += 1
        await state.set_state(Form.room_type)
        await message.answer(
            f"Type of the {users[message.chat.id].room_index + 1} room",
            reply_markup=inline.get_room_type_keyboard(
                message.chat.id,
                [
                    (str(Room.Type.KITCHEN), Room.Type.KITCHEN),
                    (str(Room.Type.BEDROOM), Room.Type.BEDROOM),
                    (str(Room.Type.LIVING_ROOM), Room.Type.LIVING_ROOM),
                ],
            ),
        )

        return

    await state.set_state(Form.extra)
    await message.answer(
        "Do you want to add something?",
        reply_markup=inline.get_yes_no_keyboard(message.chat.id, yes="Yes", no="No"),
    )

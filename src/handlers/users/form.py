from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.fsm.context import FSMContext


from src.states.form import Form
from src.models.report import Report
from src.models.room import Room


from loader import users

form_router = Router()


@form_router.message(Form.name)
async def process_name(message: types.Message, state: FSMContext) -> None:
    users[message.chat.id].name = message.text
    await state.set_state(Form.phone)
    await message.answer("Phone number")


@form_router.message(Form.phone)
async def process_phone(message: types.Message, state: FSMContext) -> None:
    users[message.chat.id].phone = message.text
    await state.set_state(Form.email)
    await message.answer("Email")


@form_router.message(Form.email)
async def process_email(message: types.Message, state: FSMContext) -> None:
    users[message.chat.id].email = message.text
    await state.set_state(Form.address)
    await message.answer("Text client's address")


@form_router.message(Form.address)
async def process_address(message: types.Message, state: FSMContext) -> None:
    users[message.chat.id].address = message.text
    await state.set_state(Form.rooms_count)
    await message.answer("Ok, text rooms count")


@form_router.message(Form.rooms_count)
async def process_rooms_count(message: types.Message, state: FSMContext) -> None:
    rooms_count = int(message.text)
    users[message.chat.id].rooms_count = rooms_count
    users[message.chat.id].rooms = [Room() for _ in range(rooms_count)]
    await state.set_state(Form.room_type)
    await message.answer(
        f"Ok, now text the type of {users[message.chat.id].room_index}",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=Room.Type.KITCHEN),
                    KeyboardButton(text=Room.Type.BEDROOM),
                    KeyboardButton(text=Room.Type.LIVING_ROOM),
                ],
                [KeyboardButton(text=Room.Type.OTHER)],
            ],
            one_time_keyboard=True,
        ),
    )


@form_router.message(Form.room_type)
async def process_rooms_type(message: types.Message, state: FSMContext) -> None:
    room_index = users[message.chat.id].room_index
    room: Room = users[message.chat.id].rooms[room_index]
    room.type = Room.Type(message.text)
    await state.set_state(Form.room_before)
    await message.answer(f"Send photo before works")


@form_router.message(Form.room_before)
async def process_room_before(message: types.Message, state: FSMContext) -> None:
    room_index = users[message.chat.id].room_index
    room: Room = users[message.chat.id].rooms[room_index]
    room.photo_before = "Photo 1"
    await state.set_state(Form.room_after)
    await message.answer(f"Send photo after works")


@form_router.message(Form.room_after)
async def process_room_after(message: types.Message, state: FSMContext) -> None:
    room_index = users[message.chat.id].room_index
    room: Room = users[message.chat.id].rooms[room_index]
    room.photo_after = "Photo 2"

    if room_index + 1 < users[message.chat.id].rooms_count:
        await state.set_state(Form.room_type)
        await message.answer(
            f"Ok, now text the type of {users[message.chat.id].room_index}",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=Room.Type.KITCHEN),
                        KeyboardButton(text=Room.Type.BEDROOM),
                        KeyboardButton(text=Room.Type.LIVING_ROOM),
                    ],
                    [KeyboardButton(text=Room.Type.OTHER)],
                ],
                one_time_keyboard=True,
            ),
        )
        return

    await state.set_state(Form.add)
    await message.answer(
        "Do you want to add something?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Yes"), KeyboardButton(text="No")]],
            one_time_keyboard=True,
        ),
    )


@form_router.message(Form.add)
async def process_add(message: types.Message, state: FSMContext) -> None:
    if message.text == "No":
        await message.answer("Ok. Thank you for your work!")
        return

    report: Report = users[message.chat.id]
    report.additional = [message.text]
    await message.answer("Thank you for your work!")

from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import re


from aiogram.fsm.context import FSMContext
from src.keyboards.reply.form import get_room_type_keyboard, get_yes_no_keyboard
from src.models import report


from src.states.form import Form
from src.models.report import Report
from src.models.room import Room


from loader import users

form_router = Router()


@form_router.message(Form.name)
async def process_name(message: types.Message, state: FSMContext) -> None:
    if not is_valid_name(message.text):
        await message.answer("Incorrect Name")
        return

    name = get_name(message.text)
    report = get_current_user_report(message)
    report.name = name
    await state.set_state(Form.phone)
    await message.answer("Phone number")


@form_router.message(Form.phone)
async def process_phone(message: types.Message, state: FSMContext) -> None:
    if not is_valid_phone(message.text):
        await message.answer("Incorrect phone")
        return

    phone = get_phone(message.text)
    report = get_current_user_report(message)
    report.phone = phone
    await state.set_state(Form.email)
    await message.answer("Email")


@form_router.message(Form.email)
async def process_email(message: types.Message, state: FSMContext) -> None:
    if not is_valid_email(message.text):
        await message.answer("Incorrect email")
        return

    email = get_email(message.text)
    report = get_current_user_report(message)
    report.email = email
    await state.set_state(Form.address)
    await message.answer("Text client's address")


@form_router.message(Form.address)
async def process_address(message: types.Message, state: FSMContext) -> None:
    if not is_valid_address(message.text):
        await message.answer("Incorrect address")
        return

    address = get_address(message.text)
    report = get_current_user_report(message)
    report.address = address
    await state.set_state(Form.comment)
    await message.answer("Ok, rooms count")


@form_router.message(Form.comment)
async def process_comment(message: types.Message, state: FSMContext) -> None:
    if not is_valid_comment(message.text):
        await message.answer("Incorrect comment")
        return
    comment = get_comment(message.text)
    report = get_current_user_report(message)
    report.comment = comment
    await state.set_state(Form.rooms_count)
    await message.answer("Ok, comment for work")


@form_router.message(Form.rooms_count)
async def process_rooms_count(message: types.Message, state: FSMContext) -> None:
    if not is_valid_rooms_count(message.text):
        await message.answer("Incorrect rooms count")
        return

    report = get_current_user_report(message)
    rooms_count = get_rooms_count(message.text)
    report.rooms_count = rooms_count
    report.rooms = [Room() for _ in range(rooms_count)]
    await state.set_state(Form.room_type)
    await message.answer(
        f"Type of the {users[message.chat.id].room_index + 1} room",
        reply_markup=get_room_type_keyboard(
            kitchen_text=Room.Type.KITCHEN,
            bedroom_text=Room.Type.BEDROOM,
            living_room_text=Room.Type.LIVING_ROOM,
            other_text=Room.Type.OTHER,
        ),
    )


@form_router.message(Form.room_type)
async def process_rooms_type(message: types.Message, state: FSMContext) -> None:
    room = get_current_user_room(message)
    room.type = Room.Type(message.text)
    await state.set_state(Form.room_before)
    await message.answer(f"Send photo before works")


@form_router.message(Form.room_before, F.photo)
async def process_room_before(message: types.Message, state: FSMContext) -> None:
    room = get_current_user_room(message)
    print(type(message.photo))
    room.photo_before = get_photo(message.photo)
    await state.set_state(Form.room_after)
    await message.answer(f"Send photo after works")


@form_router.message(Form.room_after, F.photo)
async def process_room_after(message: types.Message, state: FSMContext) -> None:
    report = get_current_user_report(message)
    room = get_current_user_room(message)
    room.photo_after = get_photo(message.photo)
    if report.room_index + 1 < users[message.chat.id].rooms_count:
        users[message.chat.id].room_index += 1
        await state.set_state(Form.room_type)
        await message.answer(
            f"Type of the {users[message.chat.id].room_index + 1} room",
            reply_markup=get_room_type_keyboard(
                kitchen_text=Room.Type.KITCHEN,
                bedroom_text=Room.Type.BEDROOM,
                living_room_text=Room.Type.LIVING_ROOM,
                other_text=Room.Type.OTHER,
            ),
        )

        return

    await state.set_state(Form.add)
    await message.answer(
        "Do you want to add something?",
        reply_markup=get_yes_no_keyboard(yes_text="Yes", no_text="No"),
    )


@form_router.message(Form.add)
async def process_add(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    if message.text == "No":
        await message.answer(
            f"Ok. Thank you for your work!\n{get_current_user_report(message)}",
            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
        )
        return

    report: Report = users[message.chat.id]
    report.additional = [message.text]
    await message.answer(
        f"Thank you for your work!\n{get_current_user_report(message)}",
        reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
    )


def get_current_user_report(message: types.Message) -> Report:
    return users[message.chat.id]


def is_valid_name(text: str | None) -> bool:
    if text is None:
        return False
    return True


def get_name(text: str | None) -> str:
    if text is None:
        return ""
    return text


def is_valid_phone(text: str | None) -> bool:
    if text is None:
        return False

    text = text.replace(" ", "").replace("+", "").replace("-", "")
    if not text.isdigit():
        return False

    return True


def get_phone(text: str | None) -> str:
    if text is None:
        return ""

    return text.replace(" ", "").replace("+", "").replace("-", "")


def is_valid_email(text: str | None) -> bool:
    if text is None:
        return False

    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if not re.fullmatch(regex, text):
        return False

    return True


def get_email(text: str | None) -> str:
    if text is None:
        return ""
    return text


def is_valid_address(text: str | None):
    if text is None:
        return False
    return True


def get_address(text: str | None) -> str:
    if text is None:
        return ""
    return text


def is_valid_comment(text: str | None) -> bool:
    if text is None:
        return False
    return True


def get_comment(text: str | None) -> str:
    if text is None:
        return ""
    return text


def is_valid_rooms_count(text: str | None) -> bool:
    if text is None:
        return False

    if not text.isdigit():
        return False

    if int(text) <= 0:
        return False
    return True


def get_rooms_count(text: str | None) -> int:
    if text is None:
        return 0
    return int(text)


def get_current_user_room(message: types.Message) -> Room:
    current_room_index = users[message.chat.id].room_index
    return users[message.chat.id].rooms[current_room_index]


def get_photo(photos: list[types.PhotoSize] | None) -> types.PhotoSize | None:
    if photos is None:
        return None
    high_resolution_photo = photos[-1]
    return high_resolution_photo

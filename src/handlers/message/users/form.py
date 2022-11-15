from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove, FSInputFile


from aiogram.fsm.context import FSMContext
from src.keyboards.reply.form import (
    get_room_type_keyboard,
    get_yes_no_keyboard,
    get_service_keyboard,
)

from src.keyboards.inline.extra import get_extra_service_keyboard


from src.states.form import Form
from src.models.report import Report
from src.models.room import Room
from src.misc.validators import (
    is_valid_address,
    is_valid_email,
    is_valid_cleaned,
    is_valid_helped_with,
    is_valid_name,
    is_valid_room_object,
    is_valid_phone,
    is_valid_room_type,
    is_valid_rooms_count,
)

from src.misc.getters import (
    get_address,
    get_cleaned,
    get_current_user_report,
    get_current_user_room,
    get_name,
    get_phone,
    get_photo,
    get_room_object,
    get_room_type,
    get_rooms_count,
)

from src.services.pdfreport import pdfGenerator

from loader import users, bot

form_router = Router()


@form_router.message(Form.name, F.text)
async def process_name(message: types.Message, state: FSMContext) -> None:
    if not is_valid_name(message.text):
        await message.answer("Incorrect Name")
        return

    name = get_name(message.text)
    report = get_current_user_report(message.chat.id)
    report.name = name
    await state.set_state(Form.phone)
    await message.answer("Enter Phone number")


@form_router.message(Form.phone, F.text)
async def process_phone(message: types.Message, state: FSMContext) -> None:
    if not is_valid_phone(message.text):
        await message.answer("Incorrect phone")
        return

    phone = get_phone(message.text)
    report = get_current_user_report(message.chat.id)
    report.phone = phone
    await state.set_state(Form.email)
    await message.answer("Enter Email:")


@form_router.message(Form.email, F.text)
async def process_email(message: types.Message, state: FSMContext) -> None:
    if not is_valid_email(message.text):
        await message.answer("Incorrect email")
        return

    email = get_email(message.text)
    report = get_current_user_report(message.chat.id)
    report.email = email
    await state.set_state(Form.address)
    await message.answer("Enter client address:")


def get_email(text: str | None) -> str:
    if text is None:
        return ""
    return text


@form_router.message(Form.address, F.text)
async def process_address(message: types.Message, state: FSMContext) -> None:
    if not is_valid_address(message.text):
        await message.answer("Incorrect address")
        return

    address = get_address(message.text)
    report = get_current_user_report(message.chat.id)
    report.address = address
    await state.set_state(Form.helped_with)
    await message.answer("Enter information what you helped with:")


@form_router.message(Form.helped_with, F.text)
async def process_comment(message: types.Message, state: FSMContext) -> None:
    if not is_valid_helped_with(message.text):
        await message.answer("Incorrect comment")
        return
    helped_with = get_helped_with(message.text)
    report = get_current_user_report(message.chat.id)
    report.helped_with = helped_with
    await state.set_state(Form.cleaned)
    await message.answer("Enter information about what you cleaned:")


def get_helped_with(text: str | None) -> str:
    if text is None:
        return ""
    return text


@form_router.message(Form.cleaned)
async def process_cleaned(message: types.Message, state: FSMContext) -> None:
    if not is_valid_cleaned(message.text):
        await message.answer("Incorrect comment")
        return
    cleaned = get_cleaned(message.text)
    report = get_current_user_report(message.chat.id)
    report.cleaned = cleaned
    await state.set_state(Form.service)
    await message.answer(
        "Choose service:",
        reply_markup=get_service_keyboard(
            full_text=Report.Service.FULL,
            base_text=Report.Service.BASE,
            without_cleaning_text=Report.Service.WITHOUT_CLEANING,
        ),
    )


@form_router.message(
    Form.service,
    F.text.in_(
        [Report.Service.FULL, Report.Service.BASE, Report.Service.WITHOUT_CLEANING]
    ),
)
async def process_service(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.extra_service)
    await message.answer(
        "Any extra services?",
        reply_markup=get_yes_no_keyboard(yes_text="Yes", no_text="No"),
    )


@form_router.message(Form.extra_service, F.text == "Yes")
async def process_extra_service_yes(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        "Choose extra services",
        reply_markup=get_extra_service_keyboard(
            chat_id=message.chat.id,
            extra_services=[
                Report.ExtraService.COLD_FOG_MACHINE_DISINFECTIONS,
                Report.ExtraService.NEW_POLYESTER_FILTERS_INSTALLATION,
                Report.ExtraService.THERMAIL_INSULATOR_CHANGE_JOB,
                Report.ExtraService.REPAIR_WORKS,
            ],
        ),
    )


@form_router.message(Form.extra_service, F.text == "No")
async def process_extra_service_no(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.rooms_count)
    await message.answer("Enter rooms count:")


@form_router.message(Form.rooms_count)
async def process_rooms_count(message: types.Message, state: FSMContext) -> None:
    if not is_valid_rooms_count(message.text):
        await message.answer("Incorrect rooms count")
        return

    report = get_current_user_report(message.chat.id)
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
        ),
    )


@form_router.message(
    Form.room_type,
    F.text.in_(
        [
            Room.Type.KITCHEN,
            Room.Type.BEDROOM,
            Room.Type.LIVING_ROOM,
        ]
    ),
)
async def process_rooms_type(message: types.Message, state: FSMContext) -> None:
    if not is_valid_room_type(message.text):
        await message.answer("Incorrect room type")
        return

    room = get_current_user_room(message.chat.id)
    room.type = get_room_type(message.text)
    await state.set_state(Form.room_object)
    await message.answer(f"Enter rooms object:")


@form_router.message(Form.room_object, F.text)
async def process_rooms_object(message: types.Message, state: FSMContext) -> None:
    if not is_valid_room_object(message.text):
        await message.answer("Incorrect comment")
        return

    room_object = get_room_object(message.text)
    room = get_current_user_room(message.chat.id)
    room.room_object = room_object
    await state.set_state(Form.room_before)
    await message.answer("Send photo before works")


@form_router.message(Form.room_before, F.photo)
async def process_room_before(message: types.Message, state: FSMContext) -> None:
    room = get_current_user_room(message.chat.id)
    room.photo_before = get_photo(message.photo)
    await state.set_state(Form.room_after)
    await message.answer(f"Send photo after works")


@form_router.message(Form.room_after, F.photo)
async def process_room_after(message: types.Message, state: FSMContext) -> None:
    report = get_current_user_report(message.chat.id)
    room = get_current_user_room(message.chat.id)
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
            ),
        )

        return

    await state.set_state(Form.extra)
    await message.answer(
        "Do you want to add something?",
        reply_markup=get_yes_no_keyboard(yes_text="Yes", no_text="No"),
    )


@form_router.message(Form.extra, F.text == "Yes")
async def process_extra_yes(message: types.Message, state: FSMContext) -> None:
    report_date = get_current_user_report(message.chat.id).date
    report_name = report_date.strftime("%m-%d-%Y_%H-%M-%S")
    pdfGenerator(report_name).generate(
        await get_current_user_report(message.chat.id).dict_with_binary(bot)
    )
    file = FSInputFile(f"./reports/{report_name}.pdf")
    await message.answer_document(
        file,
        caption="Thank you for your work!",
        reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
    )


@form_router.message(Form.extra, F.text == "No")
async def process_extra_no(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        f"Ok. Thank you for your work!\n{get_current_user_report(message.chat.id)}",
        reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
    )

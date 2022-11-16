from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


from src.models.report import Report
from src.states.form import Form
from loader import users

router = Router()


@router.message(Command(commands=["start"]))
async def command_start(message: types.Message, state: FSMContext) -> None:
    users[message.chat.id] = Report()
    await state.set_state(Form.date)
    await message.answer(
        f"Hi! {message.from_user.first_name} {message.from_user.last_name}"
    )
    await message.answer("Enter date of visit in format DAY MONTH YEAR")


@router.message(Command(commands=["cancel"]))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.clear()
    await message.answer("Cancelled!")

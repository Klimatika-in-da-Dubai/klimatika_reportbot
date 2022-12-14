from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from src.models.report import Report
from src.states.form import Form
from loader import users

router = Router()


@router.message(Command(commands=["start"]))
async def command_start(message: types.Message, state: FSMContext) -> None:
    users[message.chat.id] = Report()
    await state.set_state(Form.client_name)
    await message.answer(
        _("Hi! {first_name} {last_name}").format(
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
    )
    await message.answer(_("Enter clients Name"))


@router.message(Command(commands=["cancel"]))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.clear()
    await message.answer(_("Cancelled!"))

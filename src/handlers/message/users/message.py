from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from src.models.report import Report
from src.states.form import Form

import src.misc.getters as get
from src.states import setters as set_state

from loader import users

router = Router()


@router.message(Command(commands=["start"]))
async def command_start(message: types.Message, state: FSMContext) -> None:
    users[message.chat.id] = Report()
    await message.answer(
        _("Hi! {first_name} {last_name}").format(
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
    )
    await set_state.set_client_name_state(message, state)



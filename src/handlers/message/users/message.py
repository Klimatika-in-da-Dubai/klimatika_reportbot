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


@router.message(Form.date, Command(commands=["cancel"]))
async def cancel_date(message: types.Message, state: FSMContext) -> None:
    await set_state.set_client_name_state(message, state)


@router.message(Form.client_phone, Command(commands=["cancel"]))
async def cancel_client_phone(message: types.Message, state: FSMContext) -> None:
    await set_state.set_date_state(message, state)


@router.message(Form.client_address, Command(commands=["cancel"]))
async def cancel_client_address(message: types.Message, state: FSMContext) -> None:
    await set_state.set_client_phone_state(message, state)


@router.message(Form.service, Command(commands=["cancel"]))
async def cancel_service(message: types.Message, state: FSMContext) -> None:
    await set_state.set_client_address_state(message, state)


@router.message(Form.extra_service, Command(commands=["cancel"]))
async def cancel_extra_service(message: types.Message, state: FSMContext) -> None:
    await set_state.set_service_state(message, state)


@router.message(Form.extra_service_await_answer, Command(commands=["cancel"]))
async def cancel_extra_service_answer(
    message: types.Message, state: FSMContext
) -> None:
    await set_state.set_extra_service_state(message, state)


@router.message(Form.room_cleaning_nodes, Command(commands=["cancel"]))
async def cancel_room_cleaning_nodes(message: types.Message, state: FSMContext) -> None:
    report = get.get_current_user_report(message.chat.id)

    if len(report.rooms) > 1:
        report.rooms.pop()
        await set_state.set_add_room_state(message, state)
        return

    if report.service == Report.Service.PREMIUM_EXTRA:
        await set_state.set_extra_service_state(message, state)
    else:
        await set_state.set_service_state(message, state)


@router.message(Form.cleaning_node_await_answer, Command(commands=["cancel"]))
async def cancel_cleaning_node_answer(message: types.Message, state: FSMContext):
    await set_state.set_room_cleaning_nodes_state(message, state)


@router.message(Form.cleaning_node_img_before, Command(commands=["cancel"]))
async def cancel_img_before(message: types.Message, state: FSMContext) -> None:
    room = get.get_current_user_room(message.chat.id)

    if room._index == 0:
        await set_state.set_room_cleaning_nodes_state(message, state)
    else:
        room.nodes_queue_back()
        await set_state.set_img_before_state(message, state)


@router.message(Form.cleaning_node_img_after, Command(commands=["cancel"]))
async def cancel_img_after(message: types.Message, state: FSMContext) -> None:
    room = get.get_current_user_room(message.chat.id)

    if room._index == 0:
        room._index = len(room.nodes_queue) - 1
        await set_state.set_img_before_state(message, state)
    else:
        room.nodes_queue_back()
        await set_state.set_img_after_state(message, state)


@router.message(Form.add_room, Command(commands=["cancel"]))
async def cancel_add_room(message: types.Message, state: FSMContext) -> None:
    room = get.get_current_user_room(message.chat.id)
    room.nodes_queue_back()
    await set_state.set_img_after_state(message, state)

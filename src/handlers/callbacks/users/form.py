from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from datetime import datetime

import src.keyboards.inline as inline
from src.states import Form
from src.states import setters as set_state

import src.misc.getters as get

from src.models import Report, Client, Room, CleaningNode

from src.services.pdfreport import pdfGenerator
from src.callbackdata import (
    OtherExtraServiceCB,
    ServiceCB,
    ExtraServiceCB,
    ClientCB,
    RoomTypeCB,
    CleaningNodeCB,
    FactorCB,
)


router = Router()


@router.callback_query(Form.client_type, ClientCB.filter())
async def callback_client_type(
    callback: types.CallbackQuery,
    callback_data: ClientCB,
    state: FSMContext,
):
    await callback.answer()
    report = get.get_current_user_report(callback.message.chat.id)
    report.client.type = callback_data.type

    await state.set_state(Form.client_address)
    await callback.message.answer(_("Enter client address:"))


@router.callback_query(
    Form.service, ServiceCB.filter(F.service == Report.Service.OTHER_REPAIR_SERVICES)
)
async def callback_service(
    callback: types.CallbackQuery, state: FSMContext, callback_data: ServiceCB
):
    await callback.answer()
    report = get.get_current_user_report(callback.message.chat.id)
    report.service = callback_data.service

    await set_state.set_work_factors_state(callback.message, state)


@router.callback_query(
    Form.service, ServiceCB.filter(F.service == Report.Service.PREMIUM)
)
async def callback_service_premium(
    callback: types.CallbackQuery, state: FSMContext, callback_data: ServiceCB
):
    await callback.answer()
    report = get.get_current_user_report(callback.message.chat.id)
    report.service = callback_data.service
    await state.set_state(Form.work_factors)

    await set_state.set_work_factors_state(callback.message, state)


@router.callback_query(
    Form.service, ServiceCB.filter(F.service == Report.Service.PREMIUM_EXTRA)
)
async def callback_service_premium_extra(
    callback: types.CallbackQuery, state: FSMContext, callback_data: ServiceCB
):
    await callback.answer()
    report = get.get_current_user_report(callback.message.chat.id)
    report.service = callback_data.service

    await state.set_state(Form.extra_service)
    await inline.send_extra_service_keyboard(callback.message)


@router.callback_query(
    Form.extra_service, ExtraServiceCB.filter(F.service != Report.Service.UNKNOWN)
)
async def callback_extra_service(
    callback: types.CallbackQuery, callback_data: ExtraServiceCB
):
    report = get.get_current_user_report(callback.message.chat.id)
    service = callback_data.service

    if service in report.extra_services:
        report.extra_services.remove(service)
    else:
        report.extra_services.append(service)

    await callback.answer()
    await inline.edit_extra_service_keyboard(callback.message)


@router.callback_query(
    Form.extra_service, OtherExtraServiceCB.filter(F.action == "add")
)
async def callback_extra_service_add_other(
    callback: types.CallbackQuery, state: FSMContext
):
    await callback.answer()
    await state.set_state(Form.extra_service_await_answer)
    await callback.message.answer(_("Please type other extra service"))


@router.callback_query(
    Form.extra_service, OtherExtraServiceCB.filter(F.action == "delete")
)
async def callback_extra_service_delete_other(
    callback: types.CallbackQuery, callback_data: OtherExtraServiceCB
):
    await callback.answer()
    report = get.get_current_user_report(callback.message.chat.id)
    report.other_extra_services.pop(callback_data.id)
    await inline.edit_extra_service_keyboard(callback.message)


@router.callback_query(Form.extra_service, ExtraServiceCB.filter(F.action == "enter"))
async def callback_extra_service_enter(
    callback: types.CallbackQuery, state: FSMContext
):
    await callback.answer()
    await set_state.set_work_factors_state(callback.message, state)


@router.callback_query(Form.work_factors, FactorCB.filter(F.action == "add"))
async def callback_add_work_factor(
    callback: types.CallbackQuery, callback_data: FactorCB
):
    await callback.answer()

    report = get.get_current_user_report(callback.message.chat.id)
    factor = callback_data.factor
    report.add_factor(factor)

    await inline.edit_factors_keyboard(callback.message)


@router.callback_query(Form.work_factors, FactorCB.filter(F.action == "delete"))
async def callback_delete_work_factor(
    callback: types.CallbackQuery, callback_data: FactorCB
):
    await callback.answer()

    report = get.get_current_user_report(callback.message.chat.id)
    factor = callback_data.factor
    report.pop_factor(factor)
    await inline.edit_factors_keyboard(callback.message)


@router.callback_query(Form.work_factors, FactorCB.filter(F.action == "enter"))
async def callback_enter_work_factor(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    report = get.get_current_user_report(callback.message.chat.id)

    if report.service == Report.Service.OTHER_REPAIR_SERVICES:
        room = get.get_current_user_room(callback.message.chat.id)
        room.add_node(CleaningNode("", type=CleaningNode.Type.OTHER))
        await set_state.set_repair_img_before_state(callback.message, state)
        return

    if report.Service == Report.Service.OTHER_REPAIR_SERVICES:
        room = get.get_current_user_room(callback.message.chat.id)
        room.add_node(CleaningNode("", type=CleaningNode.Type.OTHER))
        await set_state.set_repair_img_before_state(callback.message, state)
    else:
        await set_state.set_room_cleaning_nodes_state(callback.message, state)


@router.callback_query(
    Form.room_cleaning_nodes, CleaningNodeCB.filter(F.action == "add")
)
async def callback_add_cleaning_node(
    callback: types.CallbackQuery, callback_data: CleaningNodeCB
):
    await callback.answer()

    room = get.get_current_user_room(callback.message.chat.id)
    room.add_default_node(callback_data.index)
    await inline.edit_cleaning_node_keyboard(callback.message)


@router.callback_query(
    Form.room_cleaning_nodes, CleaningNodeCB.filter(F.action == "delete")
)
async def callback_delete_cleaning_node(
    callback: types.CallbackQuery, callback_data: CleaningNodeCB
):
    await callback.answer()

    room = get.get_current_user_room(callback.message.chat.id)
    room.delete_node(callback_data.index, callback_data.type)
    await inline.edit_cleaning_node_keyboard(callback.message)


@router.callback_query(
    Form.room_cleaning_nodes, CleaningNodeCB.filter(F.action == "add_other")
)
async def callback_add_other_cleaning_node(
    callback: types.CallbackQuery, state: FSMContext
):
    await callback.answer()
    await state.set_state(Form.cleaning_node_await_answer)
    await callback.message.answer(_("Please type other cleaning node"))


@router.callback_query(
    Form.room_cleaning_nodes, CleaningNodeCB.filter(F.action == "enter")
)
async def callback_enter_cleaning_node(
    callback: types.CallbackQuery, state: FSMContext
):
    await callback.answer()

    await start_getting_photos(callback.message, state)


async def start_getting_photos(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.create_nodes_queue()
    if room.nodes_queue_empty() and room.current_node == None:
        await message.answer(_("You didn't selected cleaning nodes"))
        return

    await set_state.set_img_before_state(message, state)


@router.callback_query(Form.add_room, F.data == "yes")
async def callback_add_room_yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    report = get.get_current_user_report(callback.message.chat.id)
    report.add_room()
    if report.service == Report.Service.OTHER_REPAIR_SERVICES:
        room = get.get_current_user_room(callback.message.chat.id)
        room.add_node(CleaningNode("", type=CleaningNode.Type.OTHER))
        await set_state.set_repair_img_before_state(callback.message, state)
    else:
        await set_state.set_room_cleaning_nodes_state(callback.message, state)


@router.callback_query(Form.add_room, F.data == "no")
async def callback_add_room_yes(
    callback: types.CallbackQuery, state: FSMContext, bot: Bot
):
    await callback.answer()
    await state.clear()
    await send_pdf_report(bot, callback.message)


async def send_pdf_report(bot: Bot, message: types.Message):
    await message.answer(_("Generating..."))
    await bot.send_chat_action(message.chat.id, action="upload_document")
    pdf_report_path = await generate_report(bot, message.chat.id)
    await message.answer_document(
        types.FSInputFile(pdf_report_path), caption=_("Thank you for your work!")
    )


async def generate_report(bot: Bot, chat_id: int) -> str:
    report = get.get_current_user_report(chat_id)
    client_name = "_".join(report.client.name.split(" "))
    report_name = f"{client_name}_{datetime.now().strftime('%m-%d-%Y_%H-%M-%S')}"
    report_dict = await report.dict_with_binary(bot)
    pdfGenerator(report_name).generate(report_dict)
    return f"./reports/{report_name}-compressed.pdf"

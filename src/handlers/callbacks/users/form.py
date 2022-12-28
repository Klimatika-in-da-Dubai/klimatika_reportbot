from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from datetime import datetime

import src.keyboards.inline as inline
from src.states import Form
import src.misc.getters as get

from src.models import Report, Client, Room

from src.services.pdfreport import pdfGenerator
from src.callbackdata import (
    OtherExtraServiceCB,
    ServiceCB,
    ExtraServiceCB,
    ClientCB,
    RoomTypeCB,
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

    await state.set_state(Form.room_before_vent)
    await callback.message.answer(_("Send photo BEFORE works for grills"))


@router.callback_query(
    Form.service, ServiceCB.filter(F.service == Report.Service.PREMIUM)
)
async def callback_service_premium(
    callback: types.CallbackQuery, state: FSMContext, callback_data: ServiceCB
):
    await callback.answer()
    report = get.get_current_user_report(callback.message.chat.id)
    report.service = callback_data.service
    await state.set_state(Form.room_before_vent)

    await callback.message.answer(_("Send photo BEFORE works for grills"))


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

    await state.set_state(Form.room_before_vent)
    await callback.message.answer(_("Send photo BEFORE works for grills"))


@router.callback_query(Form.add_room, F.data == "yes")
async def callback_add_room_yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    report = get.get_current_user_report(callback.message.chat.id)
    report.add_room()
    await state.set_state(Form.room_before_vent)
    await callback.message.answer(_("Send photo BEFORE works for grills"))


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
    pdf_report = await generate_report(bot, message.chat.id)
    await message.answer_document(pdf_report, caption=_("Thank you for your work!"))


async def generate_report(bot: Bot, chat_id: int) -> types.FSInputFile:
    report = get.get_current_user_report(chat_id)
    report_name = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    report_dict = await report.dict_with_binary(bot)
    pdfGenerator(report_name).generate(report_dict)
    return types.FSInputFile(f"./reports/{report_name}-compressed.pdf")

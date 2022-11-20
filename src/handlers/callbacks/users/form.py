from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext

import src.keyboards.inline as inline
from src.states import Form
import src.misc.getters as get

from src.models.report import Report

from src.services.pdfreport import pdfGenerator

router = Router()


@router.callback_query(Form.service)
async def callback_service(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    report = get.get_current_user_report(callback.message.chat.id)
    report.service = Report.Service(callback.data)
    print(report.service)
    await state.set_state(Form.extra_service)
    await callback.message.edit_text(
        "Any extra services?",
        reply_markup=inline.get_yes_no_keyboard(
            callback.message.chat.id, yes="Yes", no="No"
        ),
    )


@router.callback_query(Form.extra_service, F.data == "enter")
@router.callback_query(Form.extra_service, F.data == "no")
async def callback_extra_service_enter(
    callback: types.CallbackQuery, state: FSMContext
):
    await callback.answer()
    await state.set_state(Form.rooms_count)
    await callback.message.answer("Enter rooms count:")


@router.callback_query(Form.extra_service, F.data == "yes")
async def callback_extra_service_yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        text="Choose extra services",
        reply_markup=inline.get_extra_service_keyboard(
            chat_id=callback.message.chat.id,
            extra_services=[
                (
                    str(Report.ExtraService.COLD_FOG_MACHINE_DISINFECTIONS),
                    Report.ExtraService.COLD_FOG_MACHINE_DISINFECTIONS,
                ),
                (
                    str(Report.ExtraService.NEW_POLYESTER_FILTERS_INSTALLATION),
                    Report.ExtraService.NEW_POLYESTER_FILTERS_INSTALLATION,
                ),
                (
                    str(Report.ExtraService.THERMAIL_INSULATOR_CHANGE_JOB),
                    Report.ExtraService.THERMAIL_INSULATOR_CHANGE_JOB,
                ),
                (
                    str(Report.ExtraService.REPAIR_WORKS),
                    Report.ExtraService.REPAIR_WORKS,
                ),
            ],
            enter="Enter",
        ),
    )


@router.callback_query(Form.extra_service)
async def callback_extra_service(callback: types.CallbackQuery):
    report = get.get_current_user_report(callback.message.chat.id)
    service = Report.ExtraService(callback.data)

    if service in report.extra_services:
        report.extra_services.remove(service)
    else:
        report.extra_services.append(service)

    await callback.answer()
    await callback.message.edit_text(
        text="Choose extra services",
        reply_markup=inline.get_extra_service_keyboard(
            chat_id=callback.message.chat.id,
            extra_services=[
                (
                    str(Report.ExtraService.COLD_FOG_MACHINE_DISINFECTIONS),
                    Report.ExtraService.COLD_FOG_MACHINE_DISINFECTIONS,
                ),
                (
                    str(Report.ExtraService.NEW_POLYESTER_FILTERS_INSTALLATION),
                    Report.ExtraService.NEW_POLYESTER_FILTERS_INSTALLATION,
                ),
                (
                    str(Report.ExtraService.THERMAIL_INSULATOR_CHANGE_JOB),
                    Report.ExtraService.THERMAIL_INSULATOR_CHANGE_JOB,
                ),
                (
                    str(Report.ExtraService.REPAIR_WORKS),
                    Report.ExtraService.REPAIR_WORKS,
                ),
            ],
            enter="Enter",
        ),
    )


@router.callback_query(Form.room_type)
async def callback_room_type(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    room = get.get_current_user_room(callback.message.chat.id)
    room.type = get.get_room_type(callback.data)
    await state.set_state(Form.room_object)
    await callback.message.edit_text(f"You've choosed {room.type}")
    await callback.message.answer(f"Enter rooms object:")


@router.callback_query(Form.extra, F.data == "no")
async def process_extra_no(
    callback: types.CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await callback.answer()
    await send_pdf_report(bot, callback.message)


@router.callback_query(Form.extra, F.data == "yes")
async def process_extra_yes(
    callback: types.CallbackQuery, state: FSMContext, bot: Bot
) -> None:
    await callback.answer()
    await send_pdf_report(bot, callback.message)


async def send_pdf_report(bot: Bot, message: types.Message):
    await message.answer("Generating...")
    await bot.send_chat_action(message.chat.id, action="upload_document")
    pdf_report = await generate_report(bot, message.chat.id)
    await message.answer_document(pdf_report, caption="Thank you for your work!")


async def generate_report(bot: Bot, chat_id: int) -> types.FSInputFile:
    report = get.get_current_user_report(chat_id)
    report_name = report.date.strftime("%m-%d-%Y_%H-%M-%S")
    report_dict = await report.dict_with_binary(bot)
    pdfGenerator(report_name).generate(report_dict)
    return types.FSInputFile(f"./reports/{report_name}.pdf")

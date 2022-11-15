from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from src.keyboards.inline.extra import get_extra_service_keyboard
from src.states.form import Form
from src.misc.getters import get_current_user_report

from src.models.report import Report

router = Router()


@router.callback_query(Form.extra_service, F.data == "enter")
async def callback_extra_service_enter(
    callback: types.CallbackQuery, state: FSMContext
):
    await callback.answer()
    await state.set_state(Form.rooms_count)
    await callback.message.answer("Enter rooms count:")


@router.callback_query(Form.extra_service)
async def callback_extra_service(callback: types.CallbackQuery):
    report = get_current_user_report(callback.message.chat.id)
    service = Report.ExtraService(callback.data)

    if service in report.extra_services:
        report.extra_services.remove(service)
    else:
        report.extra_services.append(service)

    await callback.answer()
    await callback.message.edit_text(
        text="Choose extra services",
        reply_markup=get_extra_service_keyboard(
            chat_id=callback.message.chat.id,
            extra_services=[
                str(Report.ExtraService.COLD_FOG_MACHINE_DISINFECTIONS),
                str(Report.ExtraService.NEW_POLYESTER_FILTERS_INSTALLATION),
                str(Report.ExtraService.THERMAIL_INSULATOR_CHANGE_JOB),
                str(Report.ExtraService.REPAIR_WORKS),
            ],
            enter="Enter",
        ),
    )

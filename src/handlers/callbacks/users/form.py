from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from datetime import datetime

import src.keyboards.inline as inline
from src.states import Form
from src.states import setters as set_state

import src.misc.getters as get

from src.models import Report, CleaningNode, Room

from src.services.pdfreport import pdfGenerator
from src.callbackdata import (
    OtherExtraServiceCB,
    ServiceCB,
    ExtraServiceCB,
    ClientCB,
    CleaningNodeCB,
    FactorCB,
    RoomTypeCB
)
from src.misc.utils import slugify

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
    Form.service, ServiceCB.filter(F.service == Report.Service.CHECK_LIST)
)
async def callback_service(
    callback: types.CallbackQuery, state: FSMContext, callback_data: ServiceCB
):
    await callback.answer()
    report = get.get_current_user_report(callback.message.chat.id)
    report.service = callback_data.service

    await set_state.set_work_factors_state(callback.message, state)


@router.callback_query(
    Form.service, ServiceCB.filter(F.service.in_([Report.Service.SERVICE, Report.Service.MAINTENANCE]))
)
async def callback_service_team(
    callback: types.CallbackQuery, state: FSMContext, callback_data: ServiceCB
):
    await callback.answer()

    report = get.get_current_user_report(callback.message.chat.id)
    report.service = callback_data.service
    await state.set_state(Form.add_room)

    await set_state.set_room_state(callback.message, state)


# @router.callback_query(
#     Form.service, ServiceCB.filter(F.service == Report.Service.MAINTENANCE)
# )
# async def callback_service_premium_extra(
#     callback: types.CallbackQuery, state: FSMContext, callback_data: ServiceCB
# ):
#     await callback.answer()
#     report = get.get_current_user_report(callback.message.chat.id)
#     report.service = callback_data.service

#     await state.set_state(Form.add_room)

#     await set_state.set_room_state(callback.message, state)


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



# add room
@router.callback_query(
    Form.add_room, RoomTypeCB.filter()
    )

async def callback_extra_service(
    callback: types.CallbackQuery, callback_data: RoomTypeCB, state: FSMContext):
    room_type = callback_data.type

    room = get.get_current_user_room(callback.message.chat.id)
    room.room_type = room_type.name
    room.room_object = room_type
    
    report = get.get_current_user_report(callback.message.chat.id)
    if room_type == "Unknown":

        await state.set_state(Form.add_other_room)
        await callback.message.answer(_("Enter room"))

    else:
        if report.service == Report.Service.SERVICE:
            await set_state.set_room_service_nodes_state(callback.message,state)
        elif report.service == Report.Service.MAINTENANCE:
            
            await set_state.set_room_maintenance_nodes_state(callback.message,state)
        else:
            await callback.message.answer(_("Unexpected service type"))
        
    await callback.answer()


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
    await set_state.set_room_state(callback.message, state)


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

    if report.service == Report.Service.CHECK_LIST:
        room = get.get_current_user_room(callback.message.chat.id)
        room.add_node(CleaningNode("", type=CleaningNode.Type.OTHER))
        await set_state.set_repair_img_before_state(callback.message, state)
        return

    if report.Service == Report.Service.CHECK_LIST:
        room = get.get_current_user_room(callback.message.chat.id)
        room.add_node(CleaningNode("", type=CleaningNode.Type.OTHER))
        await set_state.set_repair_img_before_state(callback.message, state)
    else:
        await set_state.set_room_service_nodes_state(callback.message, state)


@router.callback_query(
    Form.room_cleaning_nodes, CleaningNodeCB.filter(F.action == "add")
)
async def callback_add_cleaning_node(
    callback: types.CallbackQuery, callback_data: CleaningNodeCB
):
    await callback.answer()

    room = get.get_current_user_room(callback.message.chat.id)
    room.add_default_node(callback_data.index)

    report = get.get_current_user_report(callback.message.chat.id)
    # Определение состояния (SERVICE или MAINTENANCE)
    if report.service == Report.Service.SERVICE:
        await inline.edit_service_node_keyboard(callback.message)
    elif report.service == Report.Service.MAINTENANCE:
        await inline.edit_maintenance_node_keyboard(callback.message)
    else:
        print(f"Report.Service: {report.service}")

@router.callback_query(
    Form.room_cleaning_nodes, CleaningNodeCB.filter(F.action == "delete")
)
async def callback_delete_cleaning_node(
    callback: types.CallbackQuery, callback_data: CleaningNodeCB
):
    await callback.answer()

    room = get.get_current_user_room(callback.message.chat.id)
    room.delete_node(callback_data.index, callback_data.type)

    report = get.get_current_user_report(callback.message.chat.id)
    # Определение состояния (SERVICE или MAINTENANCE)
    if report.service == Report.Service.SERVICE:
        await inline.edit_service_node_keyboard(callback.message)
    elif report.service == Report.Service.MAINTENANCE:
        await inline.edit_maintenance_node_keyboard(callback.message)
    else:
        print(f"Report.Service: {report.service}")


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


@router.callback_query(Form.add_another_room, F.data == "yes")
async def callback_add_room_yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    report = get.get_current_user_report(callback.message.chat.id)
    report.add_room()
    if report.service == Report.Service.CHECK_LIST:
        room = get.get_current_user_room(callback.message.chat.id)
        room.add_node(CleaningNode("", type=CleaningNode.Type.OTHER))
        await set_state.set_repair_img_before_state(callback.message, state)
    else:
        await set_state.set_room_state(callback.message, state)


@router.callback_query(Form.add_another_room, F.data == "no")
async def callback_add_room_yes(
    callback: types.CallbackQuery, state: FSMContext, bot: Bot
):
    await callback.answer()
    await state.clear()
    try:
        await send_pdf_report(bot, callback.message)
    except Exception as e:
        await callback.message.answer(
            f"An error occurred while generating or sending the report. Please notify the administrator and forward this message..\n{datetime.now()}\n{e}\n"
        )
        raise e




# Обработчик callback для кнопки "Пропустить"
@router.callback_query(F.data == "skip")
async def skip_comment(callback: types.CallbackQuery, state: FSMContext):
    room = get.get_current_user_room(callback.message.chat.id)

    # Проверяем тип отчета
    report = get.get_current_user_report(callback.message.chat.id)


    if report.service == Report.Service.SERVICE:
    # Просто переходим к следующему шагу без комментария
        room.next_cleaning_node()

        if room.nodes_queue_empty():
            await set_state.set_add_room_state(callback.message, state)
        else:
            await state.set_state(Form.cleaning_node_img_after)
            await callback.message.answer(
                _("Send photo AFTER for") + " " + room.current_node.button_text
            )

    if report.service == Report.Service.MAINTENANCE:
        await set_state.set_add_room_state(callback.message, state)
    
    await callback.answer()


async def send_pdf_report(bot: Bot, message: types.Message):
    await message.answer(_("Generating..."))
    await bot.send_chat_action(message.chat.id, action="upload_document")
    pdf_report_path = await generate_report(bot, message.chat.id)
    await message.answer_document(
        types.FSInputFile(pdf_report_path), caption=_("Thank you for your work!")
    )


async def generate_report(bot: Bot, chat_id: int) -> str:
    report = get.get_current_user_report(chat_id)
    client_name = slugify(report.client.name, allow_unicode=True)
    report_name = f"MAINTENANCE_REPORT_{client_name}_{datetime.now().strftime('%m-%d-%Y_%H-%M-%S')}"
    report_dict = await report.dict_with_binary(bot)
    path = pdfGenerator(report_name).generate(report_dict)
    return path

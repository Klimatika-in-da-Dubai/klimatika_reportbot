from aiogram import Router, types, F
from aiogram.utils.i18n import gettext as _

from aiogram.fsm.context import FSMContext

import src.keyboards.inline as inline


from src.states.form import Form
from src.models import Report, Room, Client, CleaningNode
import src.misc.validators as vld
import src.misc.getters as get
from src.states import setters as set_state


form_router = Router()


@form_router.message(Form.client_name, F.text)
async def process_name(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_name(message.text):
        await message.answer(_("Incorrect Name"))
        return

    name = get.get_name(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.client.name = name
    await set_state.set_date_state(message, state)


@form_router.message(Form.date, F.text)
async def process_date(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_date(message.text):
        await message.answer(_("Incorrect Date"))
        return

    date = get.get_date(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.date = date
    await set_state.set_client_phone_state(message, state)


@form_router.message(Form.client_phone, F.text)
async def process_phone(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_phone(message.text):
        await message.answer(_("Incorrect phone"))
        return

    phone = get.get_phone(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.client.phone = phone
    await set_state.set_client_address_state(message, state)


@form_router.message(Form.client_address, F.text)
async def process_address(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_address(message.text):
        await message.answer(_("Incorrect address"))
        return

    address = get.get_address(message.text)
    report = get.get_current_user_report(message.chat.id)
    report.client.address = address
    await set_state.set_service_state(message, state)


@form_router.message(Form.add_other_room, F.text)
async def process_address(message: types.Message, state: FSMContext) -> None:
    if not vld.is_valid_address(message.text):
        await message.answer(_("Incorrect room"))
        return
    room_name = message.text.strip() # Получаем текст и убираем пробелы
    # Получаем текущий отчет и комнату
    room = get.get_current_user_room(message.chat.id)

    # Обновляем тип комнаты
    room.room_type = room_name
    room.room_object = room_name  # Можно также сохранить имя комнаты


    report = get.get_current_user_report(message.chat.id)
    
    if report.service == Report.Service.SERVICE:
        await set_state.set_room_service_nodes_state(message,state)
    elif report.service == Report.Service.MAINTENANCE:
        
        await set_state.set_room_maintenance_nodes_state(message,state)
    else:
        await message.answer("Unexpected service type")



@form_router.message(Form.extra_service_await_answer, F.text)
async def process_extra_service_add_other(message: types.Message, state: FSMContext):
    report = get.get_current_user_report(message.chat.id)
    report.other_extra_services.append(message.text)
    await set_state.set_extra_service_state(message, state)


@form_router.message(Form.cleaning_node_await_answer, F.text)
async def process_cleaning_node_add_other(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    if len(message.text) > 31:
        await message.answer(_("Cleaning node name is too long! Should be < 31"))
        return
    room.add_node(CleaningNode(message.text, CleaningNode.Type.OTHER))
    
    report = get.get_current_user_report(message.chat.id)
        # Определение состояния (CLEANING или TEAM)
    if report.service == Report.Service.SERVICE:
        await set_state.set_room_service_nodes_state(message,state)
    elif report.service == Report.Service.MAINTENANCE:
        
        await set_state.set_room_maintenance_nodes_state(message,state)
    else:
        await message.answer("Unexpected service type")




@form_router.message(Form.cleaning_node_img_before, F.photo)
async def process_cleaning_node_img_before(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.current_node.photo_before = get.get_photo(message.photo)
    room.next_cleaning_node()

    if room.nodes_queue_empty():
        room.create_nodes_queue()
        await set_state.set_img_after_state(message, state)
        return

    await message.answer(
        _("Send photo BEFORE for") + " " + room.current_node.button_text
    )


@form_router.message(Form.cleaning_node_img_after, F.photo)
async def process_cleaning_node_img_after(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    room.current_node.photo_after = get.get_photo(message.photo)

    # Проверяем тип отчета
    report = get.get_current_user_report(message.chat.id)
    if report.service == Report.Service.SERVICE:
        # Переход в состояние ожидания комментария для каждой ноды
        await state.set_state(Form.cleaning_node_comment)
        await inline.send_skip_keyboard(message, _("Now write a recommendation for the photo"))
    elif report.service == Report.Service.MAINTENANCE:
        # Переход к следующему узлу без запроса комментария для нод
        room.next_cleaning_node()

        if room.nodes_queue_empty():
            room = get.get_current_user_room(message.chat.id)
            if not room.room_comment == "":
                await set_state.set_add_room_state(message, state)
            else:
                await state.set_state(Form.cleaning_room_comment)
                await inline.send_skip_keyboard(message, _("Now write a recommendation for the room"))

        else:
            await state.set_state(Form.cleaning_node_img_after)
            await message.answer(_("Send photo AFTER for") + " " + room.current_node.button_text)



@form_router.message(Form.cleaning_node_comment, F.text)
async def process_cleaning_node_comment(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    
    # Проверяем тип отчета
    report = get.get_current_user_report(message.chat.id)
    
    if report.service == Report.Service.SERVICE:
        if message.text.lower() != "skip":
            room.current_node.comment = message.text  # Сохраняем комментарий для текущей ноды

        # Переход к следующему узлу уборки
        room.next_cleaning_node()

        if room.nodes_queue_empty():
            await set_state.set_add_room_state(message, state)
        else:
            await state.set_state(Form.cleaning_node_img_after)
            await message.answer(
                _("Send photo AFTER for") + " " + room.current_node.button_text
            )



@form_router.message(Form.cleaning_room_comment, F.text)
async def process_cleaning_room_comment(message: types.Message, state: FSMContext):
    room = get.get_current_user_room(message.chat.id)
    # Проверяем тип отчета
    report = get.get_current_user_report(message.chat.id)
    
    if report.service == Report.Service.MAINTENANCE:
        room.room_comment = message.text  # Сохраняем комментарий для всей комнаты

        await set_state.set_add_room_state(message, state)


from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from src.models.report import Report
from src.states.form import Form

import src.misc.getters as get
from src.states import setters as set_state
from src.models.cleaningnode import DEFAULT_SERVICE_NODES,DEFAULT_MAINTENANCE_NODES


from loader import users

router = Router()


@router.message(Form.client_name, Command(commands=["cancel"]))
async def cancel_client_name(message: types.Message, state: FSMContext) -> None:
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


# @router.message(Form.extra_service, Command(commands=["cancel"]))
# async def cancel_extra_service(message: types.Message, state: FSMContext) -> None:
#     report = get.get_current_user_report(message.chat.id)
#     report.clear_extra_services()
#     await set_state.set_service_state(message, state)

# @router.message(Form.add_room, Command(commands=["cancel"]))
# async def cancel_add_room(message: types.Message, state: FSMContext) -> None:
#     await set_state.set_service_state(message, state)


@router.message(Form.add_room, Command(commands=["cancel"]))
async def cancel_add_room(message: types.Message, state: FSMContext) -> None:
    report = get.get_current_user_report(message.chat.id)
    room = get.get_current_user_room(message.chat.id)
    print("room.room_object",room.room_object, "\n !!!count rooms",len(report.rooms),"\n rooms",report.rooms)

    # if report.service == Report.Service.CHECK_LIST:
    #     await set_state.set_add_repair_unit_state(message, state)
    #     return

    if len(report.rooms) > 1:
        # room.nodes_queue_back()
        await set_state.set_add_room_state(message, state)
        return
    
    await set_state.set_service_state(message, state)
    
    

    # room = get.get_current_user_room(message.chat.id)
    # room.nodes_queue_back()
    # await set_state.set_img_after_state(message, state)
    # await set_state.set_service_state(message, state)


@router.message(Form.extra_service_await_answer, Command(commands=["cancel"]))
async def cancel_extra_service_answer(
    message: types.Message, state: FSMContext
) -> None:
    await set_state.set_extra_service_state(message, state)
    


@router.message(Form.work_factors, Command(commands=["cancel"]))
async def cancel_working_factors(message: types.Message, state: FSMContext):
    report = get.get_current_user_report(message.chat.id)
    report.clear_working_factors()
    if report.service == Report.Service.CHECK_LIST:
        await set_state.set_extra_service_state(message, state)
        return

    await set_state.set_service_state(message, state)


@router.message(Form.room_cleaning_nodes, Command(commands=["cancel"]))
async def cancel_room_cleaning_nodes(message: types.Message, state: FSMContext) -> None:
    report = get.get_current_user_report(message.chat.id)

    if len(report.rooms) > 1:
        report.rooms.pop()
        await set_state.set_room_state(message, state)
        return

    room = get.get_current_user_room(message.chat.id)
    room.clear_all_cleaning_nodes()

    await set_state.set_room_state(message, state)


@router.message(Form.cleaning_node_await_answer, Command(commands=["cancel"]))
async def cancel_cleaning_node_answer(message: types.Message, state: FSMContext):
    await set_state.set_room_service_nodes_state(message, state)


@router.message(Form.cleaning_node_img_before, Command(commands=["cancel"]))
async def cancel_img_before(message: types.Message, state: FSMContext) -> None:
    room = get.get_current_user_room(message.chat.id)
    report = get.get_current_user_report(message.chat.id)
    print("state before ",room._index)

    if room._index == 0:
        if report.service == Report.Service.SERVICE:
            await set_state.set_room_service_nodes_state(message, state)
            return
        elif report.service == Report.Service.MAINTENANCE:
            await set_state.set_room_maintenance_nodes_state(message, state)
            return

    # await set_state.set_service_state(message, state)
    #     await set_state.set_room_service_nodes_state(message, state)
    else:
        room.nodes_queue_back()
        await set_state.set_img_before_state(message, state)


# @router.message(Form.cleaning_node_img_after, Command(commands=["cancel"]))
# async def cancel_img_after(message: types.Message, state: FSMContext) -> None:
#     room = get.get_current_user_room(message.chat.id)
#     report = get.get_current_user_report(message.chat.id)
#     print("state after ",room._index)


#     if room._index == 0:
#         if report.service == Report.Service.SERVICE:
#             nodes_queue = [node for node in DEFAULT_SERVICE_NODES]  # Заменим на список для сервиса

#         elif report.service == Report.Service.MAINTENANCE:
#             nodes_queue = [node for node in DEFAULT_MAINTENANCE_NODES]  # Заменим на список для технического обслуживания
#         room._index = len(nodes_queue) - 1
#         await set_state.set_img_before_state(message, state)
#         return
    
#     else:
#         room.nodes_queue_back()
#         await set_state.set_img_after_state(message, state)

@router.message(Form.cleaning_node_img_after, Command(commands=["cancel"]))
async def cancel_img_after(message: types.Message, state: FSMContext) -> None:
    room = get.get_current_user_room(message.chat.id)
    report = get.get_current_user_report(message.chat.id)
    print("state after ", room._index)

    # Обновляем nodes_queue внутри room, а не создаем локальную переменную
    if room._index == 0:
        room.default_cleaning_nodes
        print(room.default_cleaning_nodes)
        if report.service == Report.Service.SERVICE:
            room.default_cleaning_nodes.extend([[node, False] for node in DEFAULT_SERVICE_NODES]) # Обновляем nodes_queue внутри room
        
        #     room.nodes_queue = room.default_cleaning_nodes.extend([[node, False] for node in DEFAULT_SERVICE_NODES]) # Обновляем nodes_queue внутри room
        elif report.service == Report.Service.MAINTENANCE:
            # room.nodes_queue = [node for node in DEFAULT_MAINTENANCE_NODES]  # Обновляем nodes_queue внутри room
            room.default_cleaning_nodes.extend([[node, False] for node in DEFAULT_MAINTENANCE_NODES]) # Обновляем nodes_queue внутри room
        

        # После обновления nodes_queue, пересчитываем индекс
        room._index = len(room.nodes_queue) - 1
        # print("room.nodes_queue", room.nodes_queue)

        # Проверяем, что список не пустой перед вызовом set_img_before_state
        if room.nodes_queue:
            await set_state.set_img_before_state(message, state)
        else:
            # Логируем или обрабатываем случай пустого списка
            print("Error: nodes_queue is empty.")
        return
    else:
        # Убедитесь, что nodes_queue не пустой перед выполнением метода nodes_queue_back
        if room.nodes_queue:
            room.nodes_queue_back()
            await set_state.set_img_after_state(message, state)
        else:
            # Логируем или обрабатываем случай пустого списка
            print("Error: nodes_queue is empty.")

@router.message(Form.add_another_room, Command(commands=["cancel"]))
async def cancel_add_room(message: types.Message, state: FSMContext) -> None:
    room = get.get_current_user_room(message.chat.id)
    # print("room.room_object",room.room_object)

    if room.room_object:
        room.nodes_queue_back()
        await set_state.set_img_after_state(message, state)
        return
    
    await set_state.set_service_state(message, state)


@router.message(Form.repair_img_before, Command(commands=["cancel"]))
async def cancel_repair_img_before(message: types.Message, state: FSMContext) -> None:
    report = get.get_current_user_report(message.chat.id)
    room = get.get_current_user_room(message.chat.id)
    room.pop_cleaning_node()
    if room.cleaning_nodes_empty() and len(report.rooms) == 1:
        await set_state.set_work_factors_state(message, state)
        return
    

    

    if room.cleaning_nodes_empty():
        await set_state.set_add_room_state(message, state)
    else:
        await set_state.set_add_repair_unit_state(message, state)


@router.message(Form.repair_img_after, Command(commands=["cancel"]))
async def cancel_repair_img_before(message: types.Message, state: FSMContext) -> None:
    await set_state.set_repair_img_before_state(message, state)


@router.message(Form.add_repair_unit, Command(commands=["cancel"]))
async def cancel_add_repair_unit(message: types.Message, state: FSMContext) -> None:
    await set_state.set_repair_img_after_state(message, state)

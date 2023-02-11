from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    client_name = State()
    date = State()
    client_type = State()
    client_phone = State()
    client_address = State()

    service = State()
    extra_service = State()
    extra_service_await_answer = State()

    work_factors = State()

    room_type = State()
    room_object = State()

    room_cleaning_nodes = State()
    cleaning_node_await_answer = State()

    cleaning_node_img_before = State()
    cleaning_node_img_after = State()

    add_room = State()

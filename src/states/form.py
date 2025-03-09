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

    add_room = State()
    add_other_room = State()


    work_factors = State()

    room_type = State()
    room_object = State()

    add_repair_unit = State()
    repair_img_before = State()
    repair_img_after = State()

    room_cleaning_nodes = State()
    cleaning_node_await_answer = State()

    cleaning_node_img_before = State()
    cleaning_node_img_after = State()

    cleaning_node_comment = State()
    cleaning_room_comment = State()

    add_another_room = State()


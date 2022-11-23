from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    client_name = State()
    date = State()
    client_type = State()
    client_phone = State()
    client_address = State()

    service = State()
    extra_service = State()

    room_before_vent = State()
    room_before_duct = State()
    room_before_pallet = State()
    room_before_radiator = State()
    room_before_filter = State()
    room_before_impelers = State()

    room_after_vent = State()
    room_after_duct = State()
    room_after_pallet = State()
    room_after_radiator = State()
    room_after_filter = State()
    room_after_impelers = State()

    add_room = State()

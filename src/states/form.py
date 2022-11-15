from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    name = State()
    phone = State()
    email = State()
    address = State()
    helped_with = State()
    cleaned = State()
    service = State()
    extra_service = State()
    rooms_count = State()
    room_type = State()
    room_object = State()
    room_before = State()
    room_after = State()
    extra = State()

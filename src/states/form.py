from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    name = State()
    phone = State()
    email = State()
    address = State()
    comment = State()
    rooms_count = State()
    room_type = State()
    room_before = State()
    room_after = State()
    add = State()
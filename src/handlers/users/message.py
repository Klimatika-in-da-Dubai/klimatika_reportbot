from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=["start"]))
async def start(message: types.Message) -> None:
    await message.answer(
        f"Hi! {message.from_user.first_name} {message.from_user.last_name}"
    )

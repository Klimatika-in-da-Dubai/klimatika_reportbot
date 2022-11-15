from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN

import logging

logging.basicConfig(level=logging.INFO)


users = {}  # Need replace with DB

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()  # DON'T USE IN FINAL VERSION OF PROJECT
dp = Dispatcher(storage=storage)


def on_startup(dp: Dispatcher):
    import src.handlers.message as message_handlers
    import src.handlers.callbacks as callback_handlers

    dp.include_router(message_handlers.users.users_router)
    dp.include_router(callback_handlers.users.users_router)
    ...


async def on_shutdown():
    ...

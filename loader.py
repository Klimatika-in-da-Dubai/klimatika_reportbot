from aiogram import Bot, Dispatcher, types

from config import BOT_TOKEN

import logging

logging.basicConfig(level=logging.INFO)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def on_startup(dp: Dispatcher):
    import src.handlers as handlers

    dp.include_router(handlers.users.users_router)
    ...


async def on_shutdown():
    ...

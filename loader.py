from aiogram import Bot, Dispatcher, types

import logging

logging.basicConfig(level=logging.INFO)


bot = Bot(token="")
dp = Dispatcher()


def on_startup(dp: Dispatcher):
    ...


async def on_shutdown():
    ...

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware

from pathlib import Path
from config import BOT_TOKEN

import logging

logging.basicConfig(level=logging.INFO)


users = {}  # Need replace with DB

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()  # DON'T USE IN FINAL VERSION OF PROJECT
dp = Dispatcher(storage=storage)

I18N_DOMAIN = "mybot"

BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / "locales"

i18n = I18n(path=BASE_DIR, default_locale="en", domain="messages")


def on_startup(dp: Dispatcher):
    import src.handlers.message as message_handlers
    import src.handlers.callbacks as callback_handlers

    dp.message.middleware(SimpleI18nMiddleware(i18n=i18n))
    dp.include_router(message_handlers.users.users_router)
    dp.include_router(callback_handlers.users.users_router)
    ...


async def on_shutdown():
    ...

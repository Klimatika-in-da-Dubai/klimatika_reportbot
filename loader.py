from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from log_conf import LoggingConfig
from config import BOT_TOKEN
from log_conf import LoggingConfig
from loguru import logger
import os

# Инициализация логирования
def initialize_logs():
    # Настройка Loguru
    LoggingConfig.configure()

initialize_logs()


users = {}  # Need replace with DB

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()  # DON'T USE IN FINAL VERSION OF PROJECT
dp = Dispatcher(storage=storage)


i18n = I18n(path="locales", default_locale="en", domain="messags")


def on_startup(dp: Dispatcher):
    import src.handlers.message as message_handlers
    import src.handlers.callbacks as callback_handlers
    logger.debug("Bot is starting up...")


    dp.callback_query.middleware(SimpleI18nMiddleware(i18n=i18n))
    dp.message.middleware(SimpleI18nMiddleware(i18n=i18n))
    dp.include_router(message_handlers.users.users_router)
    dp.include_router(callback_handlers.users.users_router)

    logger.debug("Startup complete!")
    ...


async def on_shutdown():
    # Очистка ресурсов при завершении работы
    logger.debug("Shutting down the bot...")
    # Можно выполнить дополнительные действия для завершения работы
    await bot.close()
    logger.debug("Shutdown complete.")



from aiogram import Router, types

from .message import router as message_router

users_router = Router()

users_router.include_router(message_router)

from aiogram import Router, types

from .message import router as message_router
from .form import form_router

users_router = Router()

users_router.include_router(message_router)
users_router.include_router(form_router)

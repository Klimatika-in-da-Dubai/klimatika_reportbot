from aiogram import Router
from .form import router

users_router = Router()

users_router.include_router(router)

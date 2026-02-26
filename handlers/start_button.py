"""Обработчики стартовых действий: /start и возврат в главное меню."""
from aiogram import F, types
from aiogram.filters import Command

from bot_config import dp
from data_store import (
    appointments,
    user_ads,
    user_history,
    user_languages,
    user_profiles,
    user_reminders,
    user_symptoms,
)
from keyboards import get_main_menu
from handlers.common import add_to_history, get_text, safe_edit_message, tr

LOCAL = {
    "signup_history": {"ru": "👋 Регистрация в боте", "en": "👋 Registered in bot", "uz": "👋 Botda ro'yxatdan o'tdi"},
}


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_languages:
        user_languages[user_id] = "ru"

    if user_id not in user_profiles:
        user_profiles[user_id] = {}
        user_symptoms[user_id] = []
        user_reminders[user_id] = []
        user_history[user_id] = []
        user_ads[user_id] = []
        appointments[user_id] = []
        add_to_history(user_id, tr(user_id, LOCAL["signup_history"]))

    welcome_text = get_text(user_id, "welcome", name=message.from_user.first_name)

    await message.answer(
        text=welcome_text,
        reply_markup=get_main_menu(user_id),
    )


@dp.callback_query(F.data == "back_to_menu")
async def back_to_main_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "main_menu"),
        reply_markup=get_main_menu(user_id),
    )
    await callback.answer()

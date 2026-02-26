"""Обработчики раздела записи на прием к ветеринару."""
from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from handlers.common import get_text, safe_edit_message, tr

LOCAL = {
    "book_online": {"ru": "📅 Записаться онлайн", "en": "📅 Book online", "uz": "📅 Onlayn yozilish"},
    "find_clinic": {"ru": "📍 Найти клинику", "en": "📍 Find clinic", "uz": "📍 Klinikani topish"},
    "back": {"ru": "🔙 Назад", "en": "🔙 Back", "uz": "🔙 Orqaga"},
    "soon": {
        "ru": "Онлайн запись будет доступна в следующем обновлении",
        "en": "Online booking will be available in the next update",
        "uz": "Onlayn yozilish keyingi yangilanishda mavjud bo'ladi",
    },
}


@dp.callback_query(F.data == "menu_appointment")
async def appointment_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    await safe_edit_message(
        callback.message,
        get_text(user_id, "appointment_section"),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["book_online"]), callback_data="book_appointment")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["find_clinic"]), callback_data="menu_clinics")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()


@dp.callback_query(F.data == "book_appointment")
async def book_appointment(callback: types.CallbackQuery):
    await callback.answer(tr(callback.from_user.id, LOCAL["soon"]))

"""Обработчики раздела записи на прием к ветеринару."""
from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from handlers.common import get_text, safe_edit_message


@dp.callback_query(F.data == "menu_appointment")
async def appointment_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    await safe_edit_message(
        callback.message,
        get_text(user_id, "appointment_section"),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📅 Записаться онлайн", callback_data="book_appointment")],
                [InlineKeyboardButton(text="📍 Найти клинику", callback_data="menu_clinics")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()


@dp.callback_query(F.data == "book_appointment")
async def book_appointment(callback: types.CallbackQuery):
    await callback.answer("Онлайн запись будет доступна в следующем обновлении")

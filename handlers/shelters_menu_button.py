"""Обработчик кнопки раздела приютов для животных."""
from aiogram import F, types

from bot_config import dp
from data_store import user_city_context
from keyboards import create_cities_keyboard
from handlers.common import get_text, safe_edit_message


@dp.callback_query(F.data == "menu_shelters")
async def shelters_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_city_context[user_id] = "shelters"
    await safe_edit_message(
        callback.message,
        get_text(user_id, "shelters_section"),
        reply_markup=create_cities_keyboard(user_id),
    )
    await callback.answer()

"""Обработчики смены языка интерфейса бота."""
from aiogram import F, types

from bot_config import dp
from data_store import user_languages
from keyboards import create_language_keyboard
from handlers.common import add_to_history, get_text, safe_edit_message
from handlers.start_button import back_to_main_menu


@dp.callback_query(F.data == "menu_language")
async def language_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "choose_language"),
        reply_markup=create_language_keyboard(),
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("lang_"))
async def set_language(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    language = callback.data.replace("lang_", "")

    user_languages[user_id] = language
    add_to_history(user_id, f"🌍 Изменен язык на {language}")

    languages = {
        "ru": "🇷🇺 Русский",
        "en": "🇺🇸 English",
        "uz": "🇺🇿 O'zbekcha",
    }

    await callback.answer(f"Язык изменен на {languages.get(language, language)}!")
    await back_to_main_menu(callback)

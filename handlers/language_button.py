"""Обработчики смены языка интерфейса бота."""
from aiogram import F, types

from bot_config import dp
from data_store import user_languages
from keyboards import create_language_keyboard
from handlers.common import add_to_history, get_text, safe_edit_message, tr
from handlers.start_button import back_to_main_menu


@dp.callback_query(F.data == "menu_language")
async def language_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "choose_language"),
        reply_markup=create_language_keyboard(user_id),
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("lang_"))
async def set_language(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    language = callback.data.replace("lang_", "")

    user_languages[user_id] = language
    history_map = {
        "ru": f"🌍 Изменен язык на {language}",
        "en": f"🌍 Language changed to {language}",
        "uz": f"🌍 Til {language} ga o'zgartirildi",
    }
    add_to_history(user_id, tr(user_id, history_map))

    languages = {
        "ru": {"ru": "🇷🇺 Русский", "en": "🇷🇺 Russian", "uz": "🇷🇺 Ruscha"},
        "en": {"ru": "🇺🇸 Английский", "en": "🇺🇸 English", "uz": "🇺🇸 Inglizcha"},
        "uz": {"ru": "🇺🇿 Узбекский", "en": "🇺🇿 Uzbek", "uz": "🇺🇿 O'zbekcha"},
    }

    alert_map = {
        "ru": f"Язык изменен на {tr(user_id, languages.get(language, {'ru': language, 'en': language, 'uz': language}))}!",
        "en": f"Language changed to {tr(user_id, languages.get(language, {'ru': language, 'en': language, 'uz': language}))}!",
        "uz": f"Til {tr(user_id, languages.get(language, {'ru': language, 'en': language, 'uz': language}))} ga o'zgartirildi!",
    }
    await callback.answer(tr(user_id, alert_map))
    await back_to_main_menu(callback)

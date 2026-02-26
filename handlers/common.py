"""Общие функции для обработчиков: тексты, история и безопасное редактирование сообщений."""
from datetime import datetime

from aiogram.enums import ParseMode

from bot_data import TEXTS
from data_store import user_history, user_languages
from keyboards import configure_text_provider


def add_to_history(user_id, text):
    """Добавляет запись в историю пользователя"""
    if user_id not in user_history:
        user_history[user_id] = []

    timestamp = datetime.now().strftime("%d.%m %H:%M")
    user_history[user_id].append(f"[{timestamp}] {text}")

    if len(user_history[user_id]) > 50:
        user_history[user_id] = user_history[user_id][-50:]


def get_text(user_id: int, text_key: str, **kwargs) -> str:
    """Получить текст на нужном языке"""
    lang = user_languages.get(user_id, "ru")
    text_dict = TEXTS.get(text_key, {})
    text = text_dict.get(lang, text_dict.get("ru", text_key))

    if kwargs:
        text = text.format(**kwargs)

    return text


def get_user_language(user_id: int) -> str:
    return user_languages.get(user_id, "ru")


def tr(user_id: int, mapping: dict) -> str:
    lang = get_user_language(user_id)
    return mapping.get(lang, mapping.get("ru", ""))


configure_text_provider(get_text)


async def safe_edit_message(message, text, reply_markup=None, parse_mode=ParseMode.HTML):
    """Безопасное редактирование сообщения"""
    try:
        await message.edit_text(
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
        )
        return True
    except Exception:
        try:
            await message.answer(
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
            )
            return False
        except Exception:
            return False

"""Обработчики истории действий пользователя и ее очистки."""
from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from data_store import user_history
from handlers.common import add_to_history, safe_edit_message, tr

LOCAL = {
    "empty": {
        "ru": "📭 <b>История пуста</b>\n\nЗдесь будут отображаться ваши действия в боте.",
        "en": "📭 <b>History is empty</b>\n\nYour bot actions will appear here.",
        "uz": "📭 <b>Tarix bo'sh</b>\n\nBu yerda botdagi harakatlaringiz ko'rsatiladi.",
    },
    "title": {"ru": "📋 <b>История действий:</b>\n\n", "en": "📋 <b>Action history:</b>\n\n", "uz": "📋 <b>Harakatlar tarixi:</b>\n\n"},
    "clear_btn": {"ru": "🗑️ Очистить историю", "en": "🗑️ Clear history", "uz": "🗑️ Tarixni tozalash"},
    "back": {"ru": "🔙 Назад", "en": "🔙 Back", "uz": "🔙 Orqaga"},
    "cleared_alert": {"ru": "✅ История очищена!", "en": "✅ History cleared!", "uz": "✅ Tarix tozalandi!"},
    "history_cleared_log": {"ru": "🗑️ История очищена", "en": "🗑️ History cleared", "uz": "🗑️ Tarix tozalandi"},
}


@dp.callback_query(F.data == "menu_history")
async def history_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    history = user_history.get(user_id, [])

    if not history:
        text = tr(user_id, LOCAL["empty"])
    else:
        text = tr(user_id, LOCAL["title"])
        for record in history[-10:]:
            text += f"• {record}\n"

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["clear_btn"]), callback_data="clear_history")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()


@dp.callback_query(F.data == "clear_history")
async def clear_history(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_history[user_id] = []
    add_to_history(user_id, tr(user_id, LOCAL["history_cleared_log"]))

    await callback.answer(tr(user_id, LOCAL["cleared_alert"]))
    await history_menu(callback)

"""Обработчики истории действий пользователя и ее очистки."""
from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from data_store import user_history
from handlers.common import add_to_history, safe_edit_message


@dp.callback_query(F.data == "menu_history")
async def history_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    history = user_history.get(user_id, [])

    if not history:
        text = "📭 <b>История пуста</b>\n\nЗдесь будут отображаться ваши действия в боте."
    else:
        text = "📋 <b>История действий:</b>\n\n"
        for record in history[-10:]:
            text += f"• {record}\n"

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🗑️ Очистить историю", callback_data="clear_history")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()


@dp.callback_query(F.data == "clear_history")
async def clear_history(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_history[user_id] = []
    add_to_history(user_id, "🗑️ История очищена")

    await callback.answer("✅ История очищена!")
    await history_menu(callback)

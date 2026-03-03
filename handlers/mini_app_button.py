"""Обработчик открытия Mini App из меню бота."""
import os

from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from bot_config import dp
from handlers.common import tr

LOCAL = {
    "title": {
        "ru": "📱 <b>PetHelper Mini App</b>\n\nОткройте наше мини-приложение для дополнительных функций:",
        "en": "📱 <b>PetHelper Mini App</b>\n\nOpen our mini app for additional features:",
        "uz": "📱 <b>PetHelper Mini App</b>\n\nQo'shimcha imkoniyatlar uchun mini ilovani oching:",
    },
    "open": {"ru": "🚀 Открыть Mini App", "en": "🚀 Open Mini App", "uz": "🚀 Mini App ni ochish"},
    "back": {"ru": "🔙 Назад", "en": "🔙 Back", "uz": "🔙 Orqaga"},
}


@dp.callback_query(F.data == "menu_mini_app")
async def mini_app_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    web_app_url = os.getenv("WEB_APP_URL", "https://example.com/webapp")
    web_app = WebAppInfo(url=web_app_url)

    await callback.message.answer(
        tr(user_id, LOCAL["title"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["open"]), web_app=web_app)],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()

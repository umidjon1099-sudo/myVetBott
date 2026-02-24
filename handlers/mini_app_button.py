"""Обработчик открытия Mini App из меню бота."""
from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from bot_config import dp


@dp.callback_query(F.data == "menu_mini_app")
async def mini_app_menu(callback: types.CallbackQuery):
    web_app = WebAppInfo(url="https://example.com/pet-helper-app")

    await callback.message.answer(
        "📱 <b>PetHelper Mini App</b>\n\nОткройте наше мини-приложение для дополнительных функций:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🚀 Открыть Mini App", web_app=web_app)],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()

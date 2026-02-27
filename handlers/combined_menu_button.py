"""Обработчик объединенных кнопок главного меню."""
from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from handlers.common import safe_edit_message, tr

LOCAL = {
    "choose_for_clinics_shelters": {
        "ru": "Выберите раздел:",
        "en": "Choose a section:",
        "uz": "Bo'limni tanlang:",
    },
    "choose_for_pharmacies_shop": {
        "ru": "Выберите раздел:",
        "en": "Choose a section:",
        "uz": "Bo'limni tanlang:",
    },
    "clinics": {"ru": "🏥 Клиники", "en": "🏥 Clinics", "uz": "🏥 Klinikalar"},
    "shelters": {"ru": "🏠 Приюты", "en": "🏠 Shelters", "uz": "🏠 Boshpanalar"},
    "pharmacies": {"ru": "💊 Аптеки", "en": "💊 Pharmacies", "uz": "💊 Dorixonalar"},
    "pet_shop": {"ru": "🛒 Зоомагазин", "en": "🛒 Pet Shop", "uz": "🛒 Pet shop"},
    "back": {"ru": "🔙 Назад", "en": "🔙 Back", "uz": "🔙 Orqaga"},
}


@dp.callback_query(F.data == "menu_clinics_shelters")
async def clinics_shelters_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        tr(user_id, LOCAL["choose_for_clinics_shelters"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["clinics"]), callback_data="menu_clinics")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["shelters"]), callback_data="menu_shelters")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()


@dp.callback_query(F.data == "menu_pharmacies_pet_shop")
async def pharmacies_pet_shop_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        tr(user_id, LOCAL["choose_for_pharmacies_shop"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["pharmacies"]), callback_data="menu_pharmacies")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["pet_shop"]), callback_data="menu_pet_shop")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()

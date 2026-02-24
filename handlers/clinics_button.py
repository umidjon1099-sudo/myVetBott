"""Общие обработчики выбора города, карты и геопоиска для разделов клиник/аптек/приютов."""
from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from bot_data import CLINICS_DATA, PHARMACIES_DATA, SHELTERS_DATA
from keyboards import create_cities_keyboard
from handlers.common import get_text, safe_edit_message


@dp.callback_query(F.data.startswith("city_"))
async def show_city_info(callback: types.CallbackQuery):
    city_key = callback.data.replace("city_", "")
    message_text = (callback.message.text or "").lower()

    if "клиник" in message_text:
        items = CLINICS_DATA.get(city_key, [])
        title = "🏥 Клиники"
    elif "аптек" in message_text:
        items = PHARMACIES_DATA.get(city_key, [])
        title = "💊 Аптеки"
    else:
        items = SHELTERS_DATA.get(city_key, [])
        title = "🏠 Приюты"

    if not items:
        text = "❌ Информация для выбранного города пока недоступна"
    else:
        text = f"{title}:\n\n" + "\n\n".join(items)

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📍 Показать на карте", callback_data=f"show_on_map_{city_key}")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("show_on_map_"))
async def show_on_map(callback: types.CallbackQuery):
    city_key = callback.data.replace("show_on_map_", "")
    city_name = city_key.capitalize()

    await callback.message.answer(
        f"🗺 Карта для {city_name}:\n"
        f"https://www.google.com/maps/search/veterinary+clinic+{city_name}"
    )
    await callback.answer()


@dp.callback_query(F.data == "menu_pet_shop")
async def pet_shop_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "pet_shop_section"),
        reply_markup=create_cities_keyboard(),
    )
    await callback.answer()


@dp.callback_query(F.data == "find_by_location")
async def find_by_location(callback: types.CallbackQuery):
    await callback.answer("Функция геолокации будет доступна в следующем обновлении")

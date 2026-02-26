"""Общие обработчики выбора города, карты и геопоиска для разделов клиник/аптек/приютов."""
from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from bot_data import CLINICS_DATA, PHARMACIES_DATA, SHELTERS_DATA
from data_store import user_city_context
from keyboards import create_cities_keyboard
from handlers.common import get_text, safe_edit_message, tr

LOCAL = {
    "clinics": {"ru": "🏥 Клиники", "en": "🏥 Clinics", "uz": "🏥 Klinikalar"},
    "pharmacies": {"ru": "💊 Аптеки", "en": "💊 Pharmacies", "uz": "💊 Dorixonalar"},
    "shelters": {"ru": "🏠 Приюты", "en": "🏠 Shelters", "uz": "🏠 Boshpanalar"},
    "no_data": {
        "ru": "❌ Информация для выбранного города пока недоступна",
        "en": "❌ No information for this city yet",
        "uz": "❌ Tanlangan shahar uchun ma'lumot hozircha yo'q",
    },
    "show_map": {"ru": "📍 Показать на карте", "en": "📍 Show on map", "uz": "📍 Xaritada ko'rsatish"},
    "back": {"ru": "🔙 Назад", "en": "🔙 Back", "uz": "🔙 Orqaga"},
    "map_for": {"ru": "🗺 Карта для", "en": "🗺 Map for", "uz": "🗺 Xarita"},
    "geo_soon": {
        "ru": "Функция геолокации будет доступна в следующем обновлении",
        "en": "Geolocation feature will be available in the next update",
        "uz": "Geolokatsiya funksiyasi keyingi yangilanishda qo'shiladi",
    },
}


@dp.callback_query(F.data.startswith("city_"))
async def show_city_info(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    city_key = callback.data.replace("city_", "")
    section = user_city_context.get(user_id, "clinics")

    if section == "clinics":
        items = CLINICS_DATA.get(city_key, [])
        title = tr(user_id, LOCAL["clinics"])
    elif section == "pharmacies":
        items = PHARMACIES_DATA.get(city_key, [])
        title = tr(user_id, LOCAL["pharmacies"])
    else:
        items = SHELTERS_DATA.get(city_key, [])
        title = tr(user_id, LOCAL["shelters"])

    if not items:
        text = tr(user_id, LOCAL["no_data"])
    else:
        text = f"{title}:\n\n" + "\n\n".join(items)

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["show_map"]), callback_data=f"show_on_map_{city_key}")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("show_on_map_"))
async def show_on_map(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    city_key = callback.data.replace("show_on_map_", "")
    city_name = city_key.capitalize()

    await callback.message.answer(
        f"{tr(user_id, LOCAL['map_for'])} {city_name}:\n"
        f"https://www.google.com/maps/search/veterinary+clinic+{city_name}"
    )
    await callback.answer()


@dp.callback_query(F.data == "menu_pet_shop")
async def pet_shop_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_city_context[user_id] = "pet_shop"
    await safe_edit_message(
        callback.message,
        get_text(user_id, "pet_shop_section"),
        reply_markup=create_cities_keyboard(user_id),
    )
    await callback.answer()


@dp.callback_query(F.data == "find_by_location")
async def find_by_location(callback: types.CallbackQuery):
    await callback.answer(tr(callback.from_user.id, LOCAL["geo_soon"]))

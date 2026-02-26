"""Обработчики раздела кормления и выдачи рекомендаций по видам животных."""
from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from bot_data import FEEDING_INFO
from data_store import user_languages
from keyboards import create_domestic_animals_keyboard, create_feeding_keyboard
from handlers.common import get_text, safe_edit_message, tr

LOCAL = {
    "domestic_title": {
        "ru": "🏠 <b>Кормление домашних животных</b>\n\nВыберите тип животного:",
        "en": "🏠 <b>Domestic Animals Feeding</b>\n\nChoose animal type:",
        "uz": "🏠 <b>Uy hayvonlarini oziqlantirish</b>\n\nHayvon turini tanlang:",
    },
    "farm_soon": {
        "ru": "Раздел кормления сельскохозяйственных животных будет добавлен скоро",
        "en": "Farm animal feeding section will be added soon",
        "uz": "Ferma hayvonlarini oziqlantirish bo'limi tez orada qo'shiladi",
    },
    "exotic_soon": {
        "ru": "Раздел кормления экзотических животных будет добавлен скоро",
        "en": "Exotic animal feeding section will be added soon",
        "uz": "Ekzotik hayvonlarni oziqlantirish bo'limi tez orada qo'shiladi",
    },
    "info_updating": {
        "ru": "Информация обновляется...",
        "en": "Information is being updated...",
        "uz": "Ma'lumot yangilanmoqda...",
    },
    "back": {"ru": "🔙 Назад", "en": "🔙 Back", "uz": "🔙 Orqaga"},
    "main": {"ru": "🏠 Главное меню", "en": "🏠 Main menu", "uz": "🏠 Asosiy menyu"},
}


@dp.callback_query(F.data == "menu_feeding")
async def feeding_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "feeding_section"),
        reply_markup=create_feeding_keyboard(user_id),
    )
    await callback.answer()


@dp.callback_query(F.data == "feeding_domestic")
async def domestic_feeding(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        tr(user_id, LOCAL["domestic_title"]),
        reply_markup=create_domestic_animals_keyboard(user_id),
    )
    await callback.answer()


@dp.callback_query(F.data == "feeding_farm")
async def farm_feeding(callback: types.CallbackQuery):
    await callback.answer(tr(callback.from_user.id, LOCAL["farm_soon"]))


@dp.callback_query(F.data == "feeding_exotic")
async def exotic_feeding(callback: types.CallbackQuery):
    await callback.answer(tr(callback.from_user.id, LOCAL["exotic_soon"]))


@dp.callback_query(F.data.startswith("feed_"))
async def show_feeding_info(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    animal_type = callback.data.replace("feed_", "")

    info = FEEDING_INFO.get(animal_type, {}).get(
        user_languages.get(user_id, "ru"), tr(user_id, LOCAL["info_updating"])
    )

    await safe_edit_message(
        callback.message,
        info,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="feeding_domestic")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["main"]), callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()

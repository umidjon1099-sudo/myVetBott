"""Обработчики раздела кормления и выдачи рекомендаций по видам животных."""
from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from bot_data import FEEDING_INFO
from data_store import user_languages
from keyboards import create_domestic_animals_keyboard, create_feeding_keyboard
from handlers.common import get_text, safe_edit_message


@dp.callback_query(F.data == "menu_feeding")
async def feeding_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "feeding_section"),
        reply_markup=create_feeding_keyboard(),
    )
    await callback.answer()


@dp.callback_query(F.data == "feeding_domestic")
async def domestic_feeding(callback: types.CallbackQuery):
    await safe_edit_message(
        callback.message,
        "🏠 <b>Кормление домашних животных</b>\n\nВыберите тип животного:",
        reply_markup=create_domestic_animals_keyboard(),
    )
    await callback.answer()


@dp.callback_query(F.data == "feeding_farm")
async def farm_feeding(callback: types.CallbackQuery):
    await callback.answer("Раздел кормления сельскохозяйственных животных будет добавлен скоро")


@dp.callback_query(F.data == "feeding_exotic")
async def exotic_feeding(callback: types.CallbackQuery):
    await callback.answer("Раздел кормления экзотических животных будет добавлен скоро")


@dp.callback_query(F.data.startswith("feed_"))
async def show_feeding_info(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    animal_type = callback.data.replace("feed_", "")

    info = FEEDING_INFO.get(animal_type, {}).get(
        user_languages.get(user_id, "ru"), "Информация обновляется..."
    )

    await safe_edit_message(
        callback.message,
        info,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="feeding_domestic")],
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()

"""Обработчики разделов новостей и интересных фактов."""
import random

from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from bot_data import ANIMAL_FACTS
from handlers.common import get_text, safe_edit_message


@dp.callback_query(F.data == "menu_news")
async def news_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    news_list = [
        "📰 <b>Новость 1:</b> В Ташкенте открылся новый приют для бездомных животных",
        "📰 <b>Новость 2:</b> Бесплатная вакцинация собак от бешенства в Самарканде",
        "📰 <b>Новость 3:</b> Конкурс на лучший зоомагазин Узбекистана 2024",
        "📰 <b>Новость 4:</b> Новый закон о защите животных в Узбекистане",
    ]

    text = get_text(user_id, "news_section") + "\n\n" + "\n\n".join(news_list)

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Обновить новости", callback_data="menu_news")],
                [InlineKeyboardButton(text=get_text(user_id, "back_to_menu"), callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()


@dp.callback_query(F.data == "menu_facts")
async def facts_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    random_fact = random.choice(ANIMAL_FACTS)

    text = get_text(user_id, "facts_section") + f"\n\n🎲 <b>Случайный факт:</b>\n\n{random_fact}"

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🎲 Еще факт", callback_data="menu_facts")],
                [InlineKeyboardButton(text=get_text(user_id, "back_to_menu"), callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()

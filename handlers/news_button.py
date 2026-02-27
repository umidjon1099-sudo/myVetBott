"""Обработчики разделов новостей и интересных фактов."""
import random

from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from bot_data import ANIMAL_FACTS
from handlers.common import get_text, get_user_language, safe_edit_message, tr

LOCAL = {
    "news_1": {
        "ru": "📰 <b>Новость 1:</b> В Ташкенте открылся новый приют для бездомных животных",
        "en": "📰 <b>News 1:</b> A new shelter for stray animals opened in Tashkent",
        "uz": "📰 <b>Yangilik 1:</b> Toshkentda qarovsiz hayvonlar uchun yangi boshpana ochildi",
    },
    "news_2": {
        "ru": "📰 <b>Новость 2:</b> Бесплатная вакцинация собак от бешенства в Самарканде",
        "en": "📰 <b>News 2:</b> Free rabies vaccination for dogs in Samarkand",
        "uz": "📰 <b>Yangilik 2:</b> Samarqandda itlarga quturishga qarshi bepul emlash",
    },
    "news_3": {
        "ru": "📰 <b>Новость 3:</b> Конкурс на лучший зоомагазин Узбекистана 2024",
        "en": "📰 <b>News 3:</b> Contest for the best pet shop in Uzbekistan 2024",
        "uz": "📰 <b>Yangilik 3:</b> O'zbekistondagi eng yaxshi zo'odokon tanlovi 2024",
    },
    "news_4": {
        "ru": "📰 <b>Новость 4:</b> Новый закон о защите животных в Узбекистане",
        "en": "📰 <b>News 4:</b> New animal protection law in Uzbekistan",
        "uz": "📰 <b>Yangilik 4:</b> O'zbekistonda hayvonlarni himoya qilish bo'yicha yangi qonun",
    },
    "refresh": {"ru": "🔄 Обновить новости", "en": "🔄 Refresh news", "uz": "🔄 Yangiliklarni yangilash"},
    "back": {"ru": "🔙 Главное меню", "en": "🔙 Main Menu", "uz": "🔙 Asosiy menyu"},
    "random_title": {"ru": "🎲 <b>Случайный факт:</b>", "en": "🎲 <b>Random fact:</b>", "uz": "🎲 <b>Tasodifiy fakt:</b>"},
    "more_fact": {"ru": "🎲 Еще факт", "en": "🎲 More fact", "uz": "🎲 Yana fakt"},
}


@dp.callback_query(F.data == "menu_news")
async def news_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    news_list = [tr(user_id, LOCAL["news_1"]), tr(user_id, LOCAL["news_2"]), tr(user_id, LOCAL["news_3"]), tr(user_id, LOCAL["news_4"])]

    text = get_text(user_id, "news_section") + "\n\n" + "\n\n".join(news_list)

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["refresh"]), callback_data="menu_news")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()


@dp.callback_query(F.data == "menu_facts")
async def facts_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lang = get_user_language(user_id)
    facts = ANIMAL_FACTS.get(lang, ANIMAL_FACTS["ru"])
    random_fact = random.choice(facts)

    text = get_text(user_id, "facts_section") + f"\n\n{tr(user_id, LOCAL['random_title'])}\n\n{random_fact}"

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["more_fact"]), callback_data="menu_facts")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()

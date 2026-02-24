"""Обработчики раздела объявлений: публикация, просмотр и список пользователя."""
from datetime import datetime

from aiogram import F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from data_store import user_ads
from keyboards import get_ads_menu
from handlers.common import add_to_history, get_text, safe_edit_message
from handlers.states import AdStates


@dp.callback_query(F.data == "menu_ads")
async def ads_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "ads_section"),
        reply_markup=get_ads_menu(user_id),
    )
    await callback.answer()


@dp.callback_query(F.data == "post_ad")
async def post_ad(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdStates.waiting_for_ad_title)

    await safe_edit_message(
        callback.message,
        "📝 Введите заголовок объявления:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="menu_ads")]]
        ),
    )
    await callback.answer()


@dp.message(AdStates.waiting_for_ad_title)
async def process_ad_title(message: types.Message, state: FSMContext):
    await state.update_data(ad_title=message.text)
    await state.set_state(AdStates.waiting_for_ad_text)

    await message.answer(
        "📄 Введите описание:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="menu_ads")]]
        ),
    )


@dp.message(AdStates.waiting_for_ad_text)
async def process_ad_text(message: types.Message, state: FSMContext):
    await state.update_data(ad_text=message.text)
    await state.set_state(AdStates.waiting_for_ad_price)

    await message.answer(
        "💰 Введите цену (или 'Бесплатно', 'Договорная'):",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="menu_ads")]]
        ),
    )


@dp.message(AdStates.waiting_for_ad_price)
async def process_ad_price(message: types.Message, state: FSMContext):
    await state.update_data(ad_price=message.text)
    await state.set_state(AdStates.waiting_for_ad_contact)

    await message.answer(
        "📞 Введите контактную информацию (телефон или Telegram):",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="menu_ads")]]
        ),
    )


@dp.message(AdStates.waiting_for_ad_contact)
async def process_ad_contact(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()

    ad = {
        "title": data.get("ad_title"),
        "text": data.get("ad_text"),
        "price": data.get("ad_price"),
        "contact": message.text,
        "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "user_id": user_id,
    }

    if user_id not in user_ads:
        user_ads[user_id] = []

    user_ads[user_id].append(ad)
    add_to_history(user_id, f"📢 Добавлено объявление: {ad['title']}")
    await state.clear()

    ad_text = (
        "✅ <b>Объявление опубликовано!</b>\n\n"
        f"<b>Заголовок:</b> {ad['title']}\n"
        f"<b>Описание:</b> {ad['text']}\n"
        f"<b>Цена:</b> {ad['price']}\n"
        f"<b>Контакты:</b> {ad['contact']}\n"
        f"<b>Дата:</b> {ad['date']}"
    )

    await message.answer(
        ad_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_ads_menu(user_id),
    )


@dp.callback_query(F.data == "my_ads")
async def show_my_ads(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    ads = user_ads.get(user_id, [])

    if not ads:
        text = "📭 <b>У вас нет опубликованных объявлений</b>"
    else:
        text = "📋 <b>Ваши объявления:</b>\n\n"
        for i, ad in enumerate(ads, 1):
            text += f"{i}. <b>{ad['title']}</b>\n"
            text += f"   💰 {ad['price']}\n"
            text += f"   📅 {ad['date']}\n"
            text += f"   👁️ {ad['contact']}\n\n"

    await safe_edit_message(callback.message, text, reply_markup=get_ads_menu(user_id))
    await callback.answer()


@dp.callback_query(F.data == "view_ads")
async def view_ads(callback: types.CallbackQuery):
    all_ads = []
    for ads in user_ads.values():
        all_ads.extend(ads)

    if not all_ads:
        text = "📭 <b>Пока нет объявлений</b>"
    else:
        text = "📢 <b>Объявления:</b>\n\n"
        for i, ad in enumerate(all_ads[-10:], 1):
            text += f"{i}. <b>{ad.get('title', '-')}</b>\n"
            text += f"   {ad.get('text', '-')}\n"
            text += f"   💰 {ad.get('price', '-')}\n"
            text += f"   📞 {ad.get('contact', '-')}\n\n"

    await safe_edit_message(callback.message, text, reply_markup=get_ads_menu(callback.from_user.id))
    await callback.answer()

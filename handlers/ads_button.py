"""Обработчики раздела объявлений: публикация, просмотр и список пользователя."""
from datetime import datetime

from aiogram import F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from data_store import user_ads
from keyboards import get_ads_menu
from handlers.common import add_to_history, get_text, safe_edit_message, tr
from handlers.states import AdStates

LOCAL = {
    "enter_title": {"ru": "📝 Введите заголовок объявления:", "en": "📝 Enter ad title:", "uz": "📝 E'lon sarlavhasini kiriting:"},
    "enter_desc": {"ru": "📄 Введите описание:", "en": "📄 Enter description:", "uz": "📄 Tavsifni kiriting:"},
    "enter_price": {"ru": "💰 Введите цену (или 'Бесплатно', 'Договорная'):", "en": "💰 Enter price (or 'Free', 'Negotiable'):", "uz": "💰 Narxni kiriting (yoki 'Bepul', 'Kelishiladi'):"},
    "enter_contact": {"ru": "📞 Введите контактную информацию (телефон или Telegram):", "en": "📞 Enter contact info (phone or Telegram):", "uz": "📞 Aloqa ma'lumotini kiriting (telefon yoki Telegram):"},
    "cancel": {"ru": "❌ Отмена", "en": "❌ Cancel", "uz": "❌ Bekor qilish"},
    "published": {"ru": "✅ <b>Объявление опубликовано!</b>", "en": "✅ <b>Ad published!</b>", "uz": "✅ <b>E'lon joylandi!</b>"},
    "f_title": {"ru": "Заголовок", "en": "Title", "uz": "Sarlavha"},
    "f_desc": {"ru": "Описание", "en": "Description", "uz": "Tavsif"},
    "f_price": {"ru": "Цена", "en": "Price", "uz": "Narx"},
    "f_contact": {"ru": "Контакты", "en": "Contact", "uz": "Aloqa"},
    "f_date": {"ru": "Дата", "en": "Date", "uz": "Sana"},
    "no_my_ads": {"ru": "📭 <b>У вас нет опубликованных объявлений</b>", "en": "📭 <b>You have no published ads</b>", "uz": "📭 <b>Sizda e'lonlar yo'q</b>"},
    "my_ads": {"ru": "📋 <b>Ваши объявления:</b>\n\n", "en": "📋 <b>Your ads:</b>\n\n", "uz": "📋 <b>Sizning e'lonlaringiz:</b>\n\n"},
    "no_ads": {"ru": "📭 <b>Пока нет объявлений</b>", "en": "📭 <b>No ads yet</b>", "uz": "📭 <b>Hozircha e'lonlar yo'q</b>"},
    "ads": {"ru": "📢 <b>Объявления:</b>\n\n", "en": "📢 <b>Ads:</b>\n\n", "uz": "📢 <b>E'lonlar:</b>\n\n"},
    "history_added": {"ru": "📢 Добавлено объявление", "en": "📢 Ad added", "uz": "📢 E'lon qo'shildi"},
}


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
        tr(callback.from_user.id, LOCAL["enter_title"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(callback.from_user.id, LOCAL["cancel"]), callback_data="menu_ads")]]
        ),
    )
    await callback.answer()


@dp.message(AdStates.waiting_for_ad_title)
async def process_ad_title(message: types.Message, state: FSMContext):
    await state.update_data(ad_title=message.text)
    await state.set_state(AdStates.waiting_for_ad_text)

    await message.answer(
        tr(message.from_user.id, LOCAL["enter_desc"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(message.from_user.id, LOCAL["cancel"]), callback_data="menu_ads")]]
        ),
    )


@dp.message(AdStates.waiting_for_ad_text)
async def process_ad_text(message: types.Message, state: FSMContext):
    await state.update_data(ad_text=message.text)
    await state.set_state(AdStates.waiting_for_ad_price)

    await message.answer(
        tr(message.from_user.id, LOCAL["enter_price"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(message.from_user.id, LOCAL["cancel"]), callback_data="menu_ads")]]
        ),
    )


@dp.message(AdStates.waiting_for_ad_price)
async def process_ad_price(message: types.Message, state: FSMContext):
    await state.update_data(ad_price=message.text)
    await state.set_state(AdStates.waiting_for_ad_contact)

    await message.answer(
        tr(message.from_user.id, LOCAL["enter_contact"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(message.from_user.id, LOCAL["cancel"]), callback_data="menu_ads")]]
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
    add_to_history(user_id, f"{tr(user_id, LOCAL['history_added'])}: {ad['title']}")
    await state.clear()

    ad_text = (
        f"{tr(user_id, LOCAL['published'])}\n\n"
        f"<b>{tr(user_id, LOCAL['f_title'])}:</b> {ad['title']}\n"
        f"<b>{tr(user_id, LOCAL['f_desc'])}:</b> {ad['text']}\n"
        f"<b>{tr(user_id, LOCAL['f_price'])}:</b> {ad['price']}\n"
        f"<b>{tr(user_id, LOCAL['f_contact'])}:</b> {ad['contact']}\n"
        f"<b>{tr(user_id, LOCAL['f_date'])}:</b> {ad['date']}"
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
        text = tr(user_id, LOCAL["no_my_ads"])
    else:
        text = tr(user_id, LOCAL["my_ads"])
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
        text = tr(callback.from_user.id, LOCAL["no_ads"])
    else:
        text = tr(callback.from_user.id, LOCAL["ads"])
        for i, ad in enumerate(all_ads[-10:], 1):
            text += f"{i}. <b>{ad.get('title', '-')}</b>\n"
            text += f"   {ad.get('text', '-')}\n"
            text += f"   💰 {ad.get('price', '-')}\n"
            text += f"   📞 {ad.get('contact', '-')}\n\n"

    await safe_edit_message(callback.message, text, reply_markup=get_ads_menu(callback.from_user.id))
    await callback.answer()

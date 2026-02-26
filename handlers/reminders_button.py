"""Обработчики раздела напоминаний: создание, сохранение и просмотр."""
from datetime import datetime

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from data_store import user_reminders
from keyboards import create_reminder_keyboard, get_reminders_menu
from handlers.common import add_to_history, get_text, safe_edit_message, tr
from handlers.states import ReminderStates

LOCAL = {
    "enter_text": {"ru": "📝 Введите текст напоминания:", "en": "📝 Enter reminder text:", "uz": "📝 Eslatma matnini kiriting:"},
    "enter_date": {"ru": "📅 Введите дату в формате ДД.ММ.ГГГГ:", "en": "📅 Enter date in DD.MM.YYYY format:", "uz": "📅 Sanani KK.OO.YYYY formatida kiriting:"},
    "cancel": {"ru": "❌ Отмена", "en": "❌ Cancel", "uz": "❌ Bekor qilish"},
    "added": {"ru": "✅ <b>Напоминание добавлено!</b>", "en": "✅ <b>Reminder added!</b>", "uz": "✅ <b>Eslatma qo'shildi!</b>"},
    "empty": {"ru": "📭 <b>У вас нет напоминаний</b>", "en": "📭 <b>You have no reminders</b>", "uz": "📭 <b>Sizda eslatmalar yo'q</b>"},
    "title": {"ru": "📋 <b>Ваши напоминания:</b>\n\n", "en": "📋 <b>Your reminders:</b>\n\n", "uz": "📋 <b>Sizning eslatmalaringiz:</b>\n\n"},
    "history_added": {"ru": "⏰ Добавлено напоминание", "en": "⏰ Reminder added", "uz": "⏰ Eslatma qo'shildi"},
}


@dp.callback_query(F.data == "menu_reminders")
async def reminders_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "reminders_section"),
        reply_markup=get_reminders_menu(user_id),
    )
    await callback.answer()


@dp.callback_query(F.data == "reminder_add")
async def add_reminder(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.set_state(ReminderStates.waiting_for_reminder_type)

    await safe_edit_message(
        callback.message,
        get_text(user_id, "reminder_types"),
        reply_markup=create_reminder_keyboard(user_id),
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("reminder_"))
async def process_reminder_type(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "reminder_add":
        return

    reminder_type = callback.data
    await state.update_data(reminder_type=reminder_type)
    await state.set_state(ReminderStates.waiting_for_reminder_text)

    await safe_edit_message(
        callback.message,
        tr(callback.from_user.id, LOCAL["enter_text"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(callback.from_user.id, LOCAL["cancel"]), callback_data="menu_reminders")]]
        ),
    )
    await callback.answer()


@dp.message(ReminderStates.waiting_for_reminder_text)
async def process_reminder_text(message: types.Message, state: FSMContext):
    await state.update_data(reminder_text=message.text)
    await state.set_state(ReminderStates.waiting_for_reminder_date)

    await message.answer(
        tr(message.from_user.id, LOCAL["enter_date"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(message.from_user.id, LOCAL["cancel"]), callback_data="menu_reminders")]]
        ),
    )


@dp.message(ReminderStates.waiting_for_reminder_date)
async def process_reminder_date(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()

    reminder = {
        "type": data.get("reminder_type"),
        "text": data.get("reminder_text"),
        "date": message.text,
        "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    }

    if user_id not in user_reminders:
        user_reminders[user_id] = []
    user_reminders[user_id].append(reminder)

    await state.clear()
    add_to_history(user_id, f"{tr(user_id, LOCAL['history_added'])}: {reminder['text']}")

    await message.answer(
        tr(user_id, LOCAL["added"]),
        reply_markup=get_reminders_menu(user_id),
    )


@dp.callback_query(F.data == "reminder_list")
async def show_reminders(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    reminders = user_reminders.get(user_id, [])

    if not reminders:
        text = tr(user_id, LOCAL["empty"])
    else:
        text = tr(user_id, LOCAL["title"])
        for i, rem in enumerate(reminders, 1):
            text += f"{i}. {rem['text']}\n"
            text += f"   📅 {rem['date']}\n"
            text += f"   🔄 {rem['type']}\n\n"

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=get_reminders_menu(user_id),
    )
    await callback.answer()

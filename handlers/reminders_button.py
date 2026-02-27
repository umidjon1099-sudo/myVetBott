"""Обработчики раздела напоминаний: быстрый и удобный сценарий создания."""
from datetime import datetime, timedelta

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
    "pick_date": {
        "ru": "📅 Выберите дату:",
        "en": "📅 Choose a date:",
        "uz": "📅 Sanani tanlang:",
    },
    "enter_date": {
        "ru": "📅 Введите дату в формате ДД.ММ.ГГГГ:",
        "en": "📅 Enter date in DD.MM.YYYY format:",
        "uz": "📅 Sanani KK.OO.YYYY formatida kiriting:",
    },
    "pick_time": {
        "ru": "🕒 Выберите время:",
        "en": "🕒 Choose time:",
        "uz": "🕒 Vaqtni tanlang:",
    },
    "enter_time": {
        "ru": "🕒 Введите время в формате ЧЧ:ММ (например, 09:30):",
        "en": "🕒 Enter time in HH:MM format (e.g., 09:30):",
        "uz": "🕒 Vaqtni SS:DD formatida kiriting (masalan, 09:30):",
    },
    "pick_days": {
        "ru": "📆 Выберите день недели или шаблон:",
        "en": "📆 Choose weekday or preset:",
        "uz": "📆 Hafta kunini yoki andozani tanlang:",
    },
    "enter_days": {
        "ru": "📆 Введите дни недели через запятую (напр: пн,ср,пт):",
        "en": "📆 Enter weekdays separated by comma (e.g., mon,wed,fri):",
        "uz": "📆 Hafta kunlarini vergul bilan kiriting (mas: du,chor,ju):",
    },
    "invalid_date": {
        "ru": "❌ Неверная дата. Используйте формат ДД.ММ.ГГГГ.",
        "en": "❌ Invalid date. Use DD.MM.YYYY format.",
        "uz": "❌ Sana noto'g'ri. KK.OO.YYYY formatidan foydalaning.",
    },
    "invalid_time": {
        "ru": "❌ Неверное время. Используйте формат ЧЧ:ММ.",
        "en": "❌ Invalid time. Use HH:MM format.",
        "uz": "❌ Vaqt noto'g'ri. SS:DD formatidan foydalaning.",
    },
    "cancel": {"ru": "❌ Отмена", "en": "❌ Cancel", "uz": "❌ Bekor qilish"},
    "added": {"ru": "✅ <b>Напоминание добавлено!</b>", "en": "✅ <b>Reminder added!</b>", "uz": "✅ <b>Eslatma qo'shildi!</b>"},
    "empty": {"ru": "📭 <b>У вас нет напоминаний</b>", "en": "📭 <b>You have no reminders</b>", "uz": "📭 <b>Sizda eslatmalar yo'q</b>"},
    "title": {"ru": "📋 <b>Ваши напоминания:</b>\n\n", "en": "📋 <b>Your reminders:</b>\n\n", "uz": "📋 <b>Sizning eslatmalaringiz:</b>\n\n"},
    "history_added": {"ru": "⏰ Добавлено напоминание", "en": "⏰ Reminder added", "uz": "⏰ Eslatma qo'shildi"},
    "back": {"ru": "🔙 Назад", "en": "🔙 Back", "uz": "🔙 Orqaga"},
    "main_menu": {"ru": "🏠 Главное меню", "en": "🏠 Main Menu", "uz": "🏠 Asosiy menyu"},
    "today": {"ru": "📅 Сегодня", "en": "📅 Today", "uz": "📅 Bugun"},
    "tomorrow": {"ru": "📅 Завтра", "en": "📅 Tomorrow", "uz": "📅 Ertaga"},
    "custom_date": {"ru": "✍️ Ввести дату", "en": "✍️ Enter date", "uz": "✍️ Sana kiritish"},
    "custom_days": {"ru": "✍️ Ввести дни", "en": "✍️ Enter days", "uz": "✍️ Kunlarni kiritish"},
    "custom_time": {"ru": "✍️ Ввести время", "en": "✍️ Enter time", "uz": "✍️ Vaqt kiritish"},
    "days_weekdays": {"ru": "Пн-Пт", "en": "Mon-Fri", "uz": "Du-Ju"},
    "days_weekend": {"ru": "Сб-Вс", "en": "Sat-Sun", "uz": "Sha-Ya"},
    "days_mon": {"ru": "Понедельник", "en": "Monday", "uz": "Dushanba"},
    "days_tue": {"ru": "Вторник", "en": "Tuesday", "uz": "Seshanba"},
    "days_wed": {"ru": "Среда", "en": "Wednesday", "uz": "Chorshanba"},
    "days_thu": {"ru": "Четверг", "en": "Thursday", "uz": "Payshanba"},
    "days_fri": {"ru": "Пятница", "en": "Friday", "uz": "Juma"},
    "days_sat": {"ru": "Суббота", "en": "Saturday", "uz": "Shanba"},
    "days_sun": {"ru": "Воскресенье", "en": "Sunday", "uz": "Yakshanba"},
    "type_one_time": {"ru": "Один раз", "en": "One time", "uz": "Bir marta"},
    "type_daily": {"ru": "Ежедневно", "en": "Daily", "uz": "Har kuni"},
    "type_weekly": {"ru": "Еженедельно", "en": "Weekly", "uz": "Har hafta"},
}

REMINDER_TYPES = {"reminder_one_time", "reminder_daily", "reminder_weekly"}


def _cancel_kb(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=tr(user_id, LOCAL["cancel"]), callback_data="menu_reminders")]]
    )


def _date_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=tr(user_id, LOCAL["today"]), callback_data="rem_date_today")],
            [InlineKeyboardButton(text=tr(user_id, LOCAL["tomorrow"]), callback_data="rem_date_tomorrow")],
            [InlineKeyboardButton(text=tr(user_id, LOCAL["custom_date"]), callback_data="rem_date_custom")],
            [InlineKeyboardButton(text=tr(user_id, LOCAL["cancel"]), callback_data="menu_reminders")],
        ]
    )


def _time_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="08:00", callback_data="rem_time_08_00"),
                InlineKeyboardButton(text="12:00", callback_data="rem_time_12_00"),
            ],
            [
                InlineKeyboardButton(text="18:00", callback_data="rem_time_18_00"),
                InlineKeyboardButton(text="21:00", callback_data="rem_time_21_00"),
            ],
            [InlineKeyboardButton(text=tr(user_id, LOCAL["custom_time"]), callback_data="rem_time_custom")],
            [InlineKeyboardButton(text=tr(user_id, LOCAL["cancel"]), callback_data="menu_reminders")],
        ]
    )


def _weekly_days_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=tr(user_id, LOCAL["days_weekdays"]), callback_data="rem_days_weekdays")],
            [InlineKeyboardButton(text=tr(user_id, LOCAL["days_weekend"]), callback_data="rem_days_weekend")],
            [
                InlineKeyboardButton(text=tr(user_id, LOCAL["days_mon"]), callback_data="rem_days_mon"),
                InlineKeyboardButton(text=tr(user_id, LOCAL["days_tue"]), callback_data="rem_days_tue"),
            ],
            [
                InlineKeyboardButton(text=tr(user_id, LOCAL["days_wed"]), callback_data="rem_days_wed"),
                InlineKeyboardButton(text=tr(user_id, LOCAL["days_thu"]), callback_data="rem_days_thu"),
            ],
            [
                InlineKeyboardButton(text=tr(user_id, LOCAL["days_fri"]), callback_data="rem_days_fri"),
                InlineKeyboardButton(text=tr(user_id, LOCAL["days_sat"]), callback_data="rem_days_sat"),
            ],
            [InlineKeyboardButton(text=tr(user_id, LOCAL["days_sun"]), callback_data="rem_days_sun")],
            [InlineKeyboardButton(text=tr(user_id, LOCAL["custom_days"]), callback_data="rem_days_custom")],
            [InlineKeyboardButton(text=tr(user_id, LOCAL["cancel"]), callback_data="menu_reminders")],
        ]
    )


def _validate_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def _validate_time(value: str) -> bool:
    try:
        datetime.strptime(value, "%H:%M")
        return True
    except ValueError:
        return False


def _one_time_date(token: str) -> str:
    today = datetime.now()
    if token == "today":
        return today.strftime("%d.%m.%Y")
    if token == "tomorrow":
        return (today + timedelta(days=1)).strftime("%d.%m.%Y")
    return today.strftime("%d.%m.%Y")


def _days_label(user_id: int, token: str) -> str:
    mapping = {
        "weekdays": tr(user_id, LOCAL["days_weekdays"]),
        "weekend": tr(user_id, LOCAL["days_weekend"]),
        "mon": tr(user_id, LOCAL["days_mon"]),
        "tue": tr(user_id, LOCAL["days_tue"]),
        "wed": tr(user_id, LOCAL["days_wed"]),
        "thu": tr(user_id, LOCAL["days_thu"]),
        "fri": tr(user_id, LOCAL["days_fri"]),
        "sat": tr(user_id, LOCAL["days_sat"]),
        "sun": tr(user_id, LOCAL["days_sun"]),
    }
    return mapping.get(token, token)


def _type_label(user_id: int, reminder_type: str) -> str:
    mapping = {
        "reminder_one_time": tr(user_id, LOCAL["type_one_time"]),
        "reminder_daily": tr(user_id, LOCAL["type_daily"]),
        "reminder_weekly": tr(user_id, LOCAL["type_weekly"]),
    }
    return mapping.get(reminder_type, reminder_type)


def _schedule_label(user_id: int, reminder: dict) -> str:
    reminder_type = reminder.get("type", "")
    time_value = reminder.get("time", "--:--")
    if reminder_type == "reminder_one_time":
        return f"{reminder.get('date', '--.--.----')} {time_value}"
    if reminder_type == "reminder_daily":
        return f"{tr(user_id, LOCAL['type_daily'])}: {time_value}"
    return f"{reminder.get('days', '-')} • {time_value}"


async def _save_and_finish(user_id: int, state: FSMContext, answer_func):
    data = await state.get_data()
    reminder_type = data.get("reminder_type")

    reminder = {
        "type": reminder_type,
        "text": data.get("reminder_text"),
        "date": data.get("date", ""),
        "days": data.get("days", ""),
        "time": data.get("time", ""),
        "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    }

    user_reminders.setdefault(user_id, []).append(reminder)
    await state.clear()

    add_to_history(user_id, f"{tr(user_id, LOCAL['history_added'])}: {reminder['text']}")
    summary = (
        f"{tr(user_id, LOCAL['added'])}\n\n"
        f"📝 {reminder['text']}\n"
        f"🔄 {_type_label(user_id, reminder_type)}\n"
        f"⏰ {_schedule_label(user_id, reminder)}"
    )
    await answer_func(summary, reply_markup=get_reminders_menu(user_id))


@dp.callback_query(F.data == "menu_reminders")
async def reminders_menu(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.clear()
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


@dp.callback_query(F.data.in_(REMINDER_TYPES))
async def process_reminder_type(callback: types.CallbackQuery, state: FSMContext):
    reminder_type = callback.data
    await state.update_data(reminder_type=reminder_type)
    await state.set_state(ReminderStates.waiting_for_reminder_text)

    await safe_edit_message(
        callback.message,
        tr(callback.from_user.id, LOCAL["enter_text"]),
        reply_markup=_cancel_kb(callback.from_user.id),
    )
    await callback.answer()


@dp.message(ReminderStates.waiting_for_reminder_text)
async def process_reminder_text(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    reminder_type = data.get("reminder_type")

    await state.update_data(reminder_text=message.text)
    if reminder_type == "reminder_one_time":
        await state.set_state(ReminderStates.waiting_for_reminder_date)
        await message.answer(
            tr(user_id, LOCAL["pick_date"]),
            reply_markup=_date_keyboard(user_id),
        )
        return

    if reminder_type == "reminder_weekly":
        await state.set_state(ReminderStates.waiting_for_reminder_days)
        await message.answer(
            tr(user_id, LOCAL["pick_days"]),
            reply_markup=_weekly_days_keyboard(user_id),
        )
        return

    await state.set_state(ReminderStates.waiting_for_reminder_time)
    await message.answer(
        tr(user_id, LOCAL["pick_time"]),
        reply_markup=_time_keyboard(user_id),
    )


@dp.callback_query(F.data.startswith("rem_date_"))
async def process_quick_date(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    token = callback.data.replace("rem_date_", "")
    if token == "custom":
        await state.set_state(ReminderStates.waiting_for_reminder_date)
        await safe_edit_message(
            callback.message,
            tr(user_id, LOCAL["enter_date"]),
            reply_markup=_cancel_kb(user_id),
        )
        await callback.answer()
        return

    await state.update_data(date=_one_time_date(token))
    await state.set_state(ReminderStates.waiting_for_reminder_time)
    await safe_edit_message(
        callback.message,
        tr(user_id, LOCAL["pick_time"]),
        reply_markup=_time_keyboard(user_id),
    )
    await callback.answer()


@dp.message(ReminderStates.waiting_for_reminder_date)
async def process_reminder_date(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    raw_date = message.text.strip()
    if not _validate_date(raw_date):
        await message.answer(tr(user_id, LOCAL["invalid_date"]), reply_markup=_cancel_kb(user_id))
        return

    await state.update_data(date=raw_date)
    await state.set_state(ReminderStates.waiting_for_reminder_time)
    await message.answer(
        tr(user_id, LOCAL["pick_time"]),
        reply_markup=_time_keyboard(user_id),
    )


@dp.callback_query(F.data.startswith("rem_days_"))
async def process_quick_days(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    token = callback.data.replace("rem_days_", "")
    if token == "custom":
        await state.set_state(ReminderStates.waiting_for_reminder_days)
        await safe_edit_message(
            callback.message,
            tr(user_id, LOCAL["enter_days"]),
            reply_markup=_cancel_kb(user_id),
        )
        await callback.answer()
        return

    await state.update_data(days=_days_label(user_id, token))
    await state.set_state(ReminderStates.waiting_for_reminder_time)
    await safe_edit_message(
        callback.message,
        tr(user_id, LOCAL["pick_time"]),
        reply_markup=_time_keyboard(user_id),
    )
    await callback.answer()


@dp.message(ReminderStates.waiting_for_reminder_days)
async def process_reminder_days(message: types.Message, state: FSMContext):
    await state.update_data(days=message.text.strip())
    await state.set_state(ReminderStates.waiting_for_reminder_time)
    await message.answer(
        tr(message.from_user.id, LOCAL["pick_time"]),
        reply_markup=_time_keyboard(message.from_user.id),
    )


@dp.callback_query(F.data.startswith("rem_time_"))
async def process_quick_time(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    token = callback.data.replace("rem_time_", "")
    if token == "custom":
        await state.set_state(ReminderStates.waiting_for_reminder_time)
        await safe_edit_message(
            callback.message,
            tr(user_id, LOCAL["enter_time"]),
            reply_markup=_cancel_kb(user_id),
        )
        await callback.answer()
        return

    time_value = token.replace("_", ":")
    await state.update_data(time=time_value)
    await _save_and_finish(user_id, state, callback.message.answer)
    await callback.answer()


@dp.message(ReminderStates.waiting_for_reminder_time)
async def process_reminder_time(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    raw_time = message.text.strip()
    if not _validate_time(raw_time):
        await message.answer(tr(user_id, LOCAL["invalid_time"]), reply_markup=_cancel_kb(user_id))
        return

    await state.update_data(time=raw_time)
    await _save_and_finish(user_id, state, message.answer)


@dp.callback_query(F.data == "reminder_list")
async def show_reminders(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    reminders = user_reminders.get(user_id, [])

    if not reminders:
        text = tr(user_id, LOCAL["empty"])
    else:
        text = tr(user_id, LOCAL["title"])
        for i, rem in enumerate(reminders, 1):
            text += f"{i}. {rem.get('text', '-')}\n"
            text += f"   🔄 {_type_label(user_id, rem.get('type', ''))}\n"
            text += f"   ⏰ {_schedule_label(user_id, rem)}\n\n"

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="menu_reminders")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["main_menu"]), callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()

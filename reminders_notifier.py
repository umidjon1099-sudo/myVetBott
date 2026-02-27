"""Фоновый отправитель уведомлений по напоминаниям."""
import asyncio
from datetime import datetime

from data_store import user_languages, user_reminders

LOCAL = {
    "title": {
        "ru": "⏰ <b>Напоминание</b>",
        "en": "⏰ <b>Reminder</b>",
        "uz": "⏰ <b>Eslatma</b>",
    },
    "type_one_time": {"ru": "Один раз", "en": "One time", "uz": "Bir marta"},
    "type_daily": {"ru": "Ежедневно", "en": "Daily", "uz": "Har kuni"},
    "type_weekly": {"ru": "Еженедельно", "en": "Weekly", "uz": "Har hafta"},
}

# Не даем отправлять одно и то же напоминание больше одного раза в минуту.
_LAST_SENT_MINUTE = {}


def _lang(user_id: int) -> str:
    return user_languages.get(user_id, "ru")


def _tr(user_id: int, key: str) -> str:
    lang = _lang(user_id)
    return LOCAL[key].get(lang, LOCAL[key]["ru"])


def _type_label(user_id: int, reminder_type: str) -> str:
    mapping = {
        "reminder_one_time": _tr(user_id, "type_one_time"),
        "reminder_daily": _tr(user_id, "type_daily"),
        "reminder_weekly": _tr(user_id, "type_weekly"),
    }
    return mapping.get(reminder_type, reminder_type)


def _matches_weekly(days_raw: str, weekday: int) -> bool:
    if not days_raw:
        return False

    text = days_raw.lower().strip()
    compact = text.replace(" ", "")

    if compact in {"пн-пт", "mon-fri", "du-ju"}:
        return weekday in {0, 1, 2, 3, 4}
    if compact in {"сб-вс", "sat-sun", "sha-ya"}:
        return weekday in {5, 6}

    aliases = {
        0: {"пн", "понедельник", "mon", "monday", "du", "dushanba"},
        1: {"вт", "вторник", "tue", "tuesday", "se", "seshanba"},
        2: {"ср", "среда", "wed", "wednesday", "chor", "chorshanba"},
        3: {"чт", "четверг", "thu", "thursday", "pay", "payshanba"},
        4: {"пт", "пятница", "fri", "friday", "ju", "juma"},
        5: {"сб", "суббота", "sat", "saturday", "sha", "shanba"},
        6: {"вс", "воскресенье", "sun", "sunday", "ya", "yakshanba"},
    }

    tokens = []
    for piece in text.replace(";", ",").split(","):
        token = piece.strip().lower()
        if token:
            tokens.append(token)

    for token in tokens:
        if token in aliases.get(weekday, set()):
            return True
    return False


def _normalize_legacy_reminder(reminder: dict):
    """Поддержка старых напоминаний без time/days."""
    if not reminder.get("time"):
        reminder["time"] = "09:00"
    if reminder.get("type") == "reminder_weekly" and not reminder.get("days"):
        # В старом формате weekly мог храниться произвольный текст в поле date.
        reminder["days"] = reminder.get("date", "")


def _should_send_now(reminder: dict, now: datetime) -> bool:
    _normalize_legacy_reminder(reminder)
    rem_time = reminder.get("time", "")
    if rem_time != now.strftime("%H:%M"):
        return False

    rem_type = reminder.get("type")
    if rem_type == "reminder_daily":
        return True

    if rem_type == "reminder_one_time":
        rem_date = reminder.get("date", "")
        return rem_date == now.strftime("%d.%m.%Y")

    if rem_type == "reminder_weekly":
        return _matches_weekly(reminder.get("days", ""), now.weekday())

    return False


def _minute_key(reminder: dict, now: datetime) -> str:
    return f"{reminder.get('created_at', '')}|{reminder.get('type', '')}|{reminder.get('text', '')}|{now.strftime('%Y-%m-%d %H:%M')}"


def _message_text(user_id: int, reminder: dict) -> str:
    return (
        f"{_tr(user_id, 'title')}\n\n"
        f"📝 {reminder.get('text', '')}\n"
        f"🔄 {_type_label(user_id, reminder.get('type', ''))}"
    )


async def start_reminder_notifier(bot):
    """Запускает бесконечный цикл проверки и отправки уведомлений."""
    while True:
        try:
            now = datetime.now()
            for user_id, reminders in list(user_reminders.items()):
                if not reminders:
                    continue

                for reminder in list(reminders):
                    if not _should_send_now(reminder, now):
                        continue

                    dedup_key = (user_id, _minute_key(reminder, now))
                    if _LAST_SENT_MINUTE.get(dedup_key):
                        continue

                    try:
                        await bot.send_message(user_id, _message_text(user_id, reminder), parse_mode="HTML")
                        _LAST_SENT_MINUTE[dedup_key] = True
                    except Exception:
                        continue

                    if reminder.get("type") == "reminder_one_time":
                        try:
                            user_reminders[user_id].remove(reminder)
                        except ValueError:
                            pass
        except Exception:
            # Не останавливаем цикл из-за единичной ошибки.
            pass

        await asyncio.sleep(20)

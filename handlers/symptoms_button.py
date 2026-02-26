"""Кнопочный раздел проверки симптомов с поддержкой RU/EN/UZ."""
from datetime import datetime

from aiogram import F, types
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from bot_data import SYMPTOM_ANIMALS, SYMPTOM_LIBRARY
from data_store import user_languages, user_symptoms
from handlers.common import add_to_history, safe_edit_message


LOCAL_UI = {
    "choose_animal": {
        "ru": "🩺 <b>Проверка симптомов</b>\n\nВыберите животное:",
        "en": "🩺 <b>Symptom Checker</b>\n\nChoose an animal:",
        "uz": "🩺 <b>Simptomlarni tekshirish</b>\n\nHayvonni tanlang:",
    },
    "choose_symptom": {
        "ru": "Выберите симптом:",
        "en": "Choose a symptom:",
        "uz": "Simptomni tanlang:",
    },
    "possible_causes": {
        "ru": "Возможные причины",
        "en": "Possible causes",
        "uz": "Ehtimoliy sabablar",
    },
    "emergency": {
        "ru": "⚠️ <b>Экстренный симптом. Срочно обратитесь к ветеринару.</b>",
        "en": "⚠️ <b>Emergency symptom. Contact a veterinarian immediately.</b>",
        "uz": "⚠️ <b>Shoshilinch simptom. Zudlik bilan veterinarga murojaat qiling.</b>",
    },
    "back_to_animals": {"ru": "🔙 К животным", "en": "🔙 To animals", "uz": "🔙 Hayvonlarga"},
    "back_to_symptoms": {"ru": "🔙 К симптомам", "en": "🔙 To symptoms", "uz": "🔙 Simptomlarga"},
    "back_to_menu": {"ru": "🏠 Главное меню", "en": "🏠 Main Menu", "uz": "🏠 Asosiy menyu"},
    "unknown_animal": {"ru": "Неизвестное животное", "en": "Unknown animal", "uz": "Noma'lum hayvon"},
    "invalid_symptom": {"ru": "Некорректный симптом", "en": "Invalid symptom", "uz": "Noto'g'ri simptom"},
}


def _lang(user_id: int) -> str:
    return user_languages.get(user_id, "ru")


def _t(user_id: int, key: str) -> str:
    language = _lang(user_id)
    return LOCAL_UI[key].get(language, LOCAL_UI[key]["ru"])


def _animal_label(user_id: int, animal_id: str) -> str:
    language = _lang(user_id)
    animal = SYMPTOM_ANIMALS[animal_id]
    return f"{animal['emoji']} {animal['name'].get(language, animal['name']['ru'])}"


def _animals_keyboard(user_id: int) -> InlineKeyboardMarkup:
    rows = []
    for animal_id in SYMPTOM_ANIMALS:
        rows.append([InlineKeyboardButton(text=_animal_label(user_id, animal_id), callback_data=f"sym_animal_{animal_id}")])
    rows.append([InlineKeyboardButton(text=_t(user_id, "back_to_menu"), callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _symptoms_keyboard(user_id: int, animal_id: str) -> InlineKeyboardMarkup:
    language = _lang(user_id)
    rows = []
    for idx, symptom in enumerate(SYMPTOM_LIBRARY.get(animal_id, [])):
        title = symptom["title"].get(language, symptom["title"]["ru"])
        rows.append([InlineKeyboardButton(text=title, callback_data=f"sym_item_{animal_id}_{idx}")])
    rows.append([InlineKeyboardButton(text=_t(user_id, "back_to_animals"), callback_data="menu_symptoms")])
    rows.append([InlineKeyboardButton(text=_t(user_id, "back_to_menu"), callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _symptom_details(user_id: int, animal_id: str, symptom_idx: int) -> str:
    language = _lang(user_id)
    symptom = SYMPTOM_LIBRARY[animal_id][symptom_idx]
    title = symptom["title"].get(language, symptom["title"]["ru"])
    causes = symptom["causes"].get(language, symptom["causes"]["ru"])

    text = f"{_animal_label(user_id, animal_id)}\n\n<b>{title}</b>\n\n<b>{_t(user_id, 'possible_causes')}:</b>\n"
    text += "\n".join(f"• {cause}" for cause in causes)
    if symptom.get("emergency"):
        text += f"\n\n{_t(user_id, 'emergency')}"
    return text


@dp.callback_query(F.data == "menu_symptoms")
async def symptoms_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        _t(user_id, "choose_animal"),
        reply_markup=_animals_keyboard(user_id),
        parse_mode=ParseMode.HTML,
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("sym_animal_"))
async def open_animal_symptoms(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    animal_id = callback.data.replace("sym_animal_", "")

    if animal_id not in SYMPTOM_LIBRARY:
        await callback.answer(_t(user_id, "unknown_animal"), show_alert=False)
        return

    await safe_edit_message(
        callback.message,
        f"{_animal_label(user_id, animal_id)}\n\n{_t(user_id, 'choose_symptom')}",
        reply_markup=_symptoms_keyboard(user_id, animal_id),
        parse_mode=ParseMode.HTML,
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("sym_item_"))
async def open_symptom_details(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    payload = callback.data.replace("sym_item_", "")

    try:
        animal_id, idx_raw = payload.rsplit("_", 1)
        symptom_idx = int(idx_raw)
    except (ValueError, TypeError):
        await callback.answer(_t(user_id, "invalid_symptom"), show_alert=False)
        return

    if animal_id not in SYMPTOM_LIBRARY or symptom_idx >= len(SYMPTOM_LIBRARY[animal_id]):
        await callback.answer(_t(user_id, "invalid_symptom"), show_alert=False)
        return

    symptom = SYMPTOM_LIBRARY[animal_id][symptom_idx]
    language = _lang(user_id)
    symptom_title = symptom["title"].get(language, symptom["title"]["ru"])

    user_symptoms.setdefault(user_id, []).append(
        {
            "animal": animal_id,
            "symptom": symptom_title,
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
    )
    add_to_history(user_id, f"🩺 Симптом: {symptom_title}")

    await safe_edit_message(
        callback.message,
        _symptom_details(user_id, animal_id, symptom_idx),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=_t(user_id, "back_to_symptoms"), callback_data=f"sym_animal_{animal_id}")],
                [InlineKeyboardButton(text=_t(user_id, "back_to_animals"), callback_data="menu_symptoms")],
                [InlineKeyboardButton(text=_t(user_id, "back_to_menu"), callback_data="back_to_menu")],
            ]
        ),
        parse_mode=ParseMode.HTML,
    )
    await callback.answer()

"""Обработчики раздела чата с ветеринаром."""
from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from data_store import vet_profiles
from handlers.common import get_text, safe_edit_message, tr

LOCAL = {
    "no_vets_title": {
        "ru": "💬 <b>Чат с ветеринаром</b>\n\nК сожалению, в данный момент нет доступных ветеринаров онлайн.\nВы можете:\n• Найти клинику для очного приема\n• Создать профиль ветеринара, если вы специалист",
        "en": "💬 <b>Vet Chat</b>\n\nUnfortunately, there are no available vets online right now.\nYou can:\n• Find a clinic for an in-person visit\n• Create a vet profile if you are a specialist",
        "uz": "💬 <b>Veterinar bilan chat</b>\n\nAfsuski, hozircha onlayn veterinarlаr yo'q.\nSiz:\n• Klinikani topishingiz mumkin\n• Mutaxassis bo'lsangiz veterinar profilini yaratishingiz mumkin",
    },
    "clinics": {"ru": "📍 Клиники", "en": "📍 Clinics", "uz": "📍 Klinikalar"},
    "be_vet": {"ru": "👨‍⚕️ Стать ветер.", "en": "👨‍⚕️ Become a vet", "uz": "👨‍⚕️ Veterinar bo'lish"},
    "back": {"ru": "🔙 Назад", "en": "🔙 Back", "uz": "🔙 Orqaga"},
    "vet_default": {"ru": "Ветеринар", "en": "Veterinarian", "uz": "Veterinar"},
    "spec_default": {"ru": "Специалист", "en": "Specialist", "uz": "Mutaxassis"},
}


@dp.callback_query(F.data == "menu_vet_chat")
async def vet_chat_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    available_vets = [vet for vet_id, vet in vet_profiles.items() if vet_id != user_id]

    if not available_vets:
        text = tr(user_id, LOCAL["no_vets_title"])

        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["clinics"]), callback_data="menu_clinics")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["be_vet"]), callback_data="create_vet_profile")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="back_to_menu")],
            ]
        )
    else:
        text = get_text(user_id, "vet_chat_section")
        buttons = []

        for vet in available_vets[:5]:
            vet_name = vet.get("vet_name", tr(user_id, LOCAL["vet_default"]))
            vet_spec = vet.get("vet_specialization", tr(user_id, LOCAL["spec_default"]))
            vet_id = list(vet_profiles.keys())[list(vet_profiles.values()).index(vet)]
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"👨‍⚕️ {vet_name} ({vet_spec})",
                        callback_data=f"chat_with_{vet_id}",
                    )
                ]
            )

        buttons.append([InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="back_to_menu")])
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    await safe_edit_message(callback.message, text, reply_markup=markup)
    await callback.answer()

"""Обработчики раздела чата с ветеринаром."""
from aiogram import F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from data_store import vet_profiles
from handlers.common import get_text, safe_edit_message


@dp.callback_query(F.data == "menu_vet_chat")
async def vet_chat_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    available_vets = [vet for vet_id, vet in vet_profiles.items() if vet_id != user_id]

    if not available_vets:
        text = "💬 <b>Чат с ветеринаром</b>\n\n"
        text += "К сожалению, в данный момент нет доступных ветеринаров онлайн.\n"
        text += "Вы можете:\n"
        text += "• Найти клинику для очного приема\n"
        text += "• Создать профиль ветеринара, если вы специалист"

        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📍 Клиники", callback_data="menu_clinics")],
                [InlineKeyboardButton(text="👨‍⚕️ Стать ветер.", callback_data="create_vet_profile")],
                [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")],
            ]
        )
    else:
        text = get_text(user_id, "vet_chat_section")
        buttons = []

        for vet in available_vets[:5]:
            vet_name = vet.get("vet_name", "Ветеринар")
            vet_spec = vet.get("vet_specialization", "Специалист")
            vet_id = list(vet_profiles.keys())[list(vet_profiles.values()).index(vet)]
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"👨‍⚕️ {vet_name} ({vet_spec})",
                        callback_data=f"chat_with_{vet_id}",
                    )
                ]
            )

        buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")])
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    await safe_edit_message(callback.message, text, reply_markup=markup)
    await callback.answer()

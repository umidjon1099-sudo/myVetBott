"""Обработчики проверки симптомов и выдачи базовых рекомендаций."""
from aiogram import F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from data_store import user_symptoms
from keyboards import create_animal_type_keyboard
from handlers.common import add_to_history, get_text, safe_edit_message
from handlers.states import SymptomsStates


@dp.callback_query(F.data == "menu_symptoms")
async def symptoms_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "symptoms_section"),
        reply_markup=create_animal_type_keyboard(),
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("animal_"))
async def process_animal_type(callback: types.CallbackQuery, state: FSMContext):
    animal_type = callback.data.replace("animal_", "")

    await state.update_data(pet_type=animal_type)
    await state.set_state(SymptomsStates.waiting_for_symptoms)

    animal_names = {
        "dog": "собаки",
        "cat": "кошки",
        "rodent": "грызуна",
        "bird": "птицы",
        "fish": "рыбок",
    }

    animal_name = animal_names.get(animal_type, "животного")

    await safe_edit_message(
        callback.message,
        f"🩺 <b>Проверка симптомов у {animal_name}</b>\n\n"
        "Опишите симптомы вашего питомца (что вас беспокоит, как давно, дополнительные детали):",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="menu_symptoms")]]
        ),
    )
    await callback.answer()


@dp.message(SymptomsStates.waiting_for_symptoms)
async def process_symptoms(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()

    symptoms_text = message.text
    pet_type = data.get("pet_type", "неизвестно")

    if user_id not in user_symptoms:
        user_symptoms[user_id] = []

    user_symptoms[user_id].append(
        {
            "pet_type": pet_type,
            "symptoms": symptoms_text,
        }
    )

    add_to_history(user_id, f"🩺 Добавлены симптомы: {symptoms_text[:50]}...")

    response = "🩺 <b>Рекомендации по симптомам:</b>\n\n"

    if any(word in symptoms_text.lower() for word in ["рвота", "понос", "диарея"]):
        response += "⚠️ <b>Симптомы могут указывать на отравление или инфекцию.</b>\n"
        response += "• Обеспечьте доступ к воде\n• Не кормите 12-24 часа\n• Срочно обратитесь к ветеринару\n\n"
    elif any(word in symptoms_text.lower() for word in ["не ест", "аппетит", "отказ"]):
        response += "⚠️ <b>Отказ от еды может быть признаком различных заболеваний.</b>\n"
        response += "• Проверьте температуру\n• Предложите любимое лакомство\n• Если не ест более 24 часов - к врачу\n\n"
    elif any(word in symptoms_text.lower() for word in ["чешется", "зуд", "аллергия"]):
        response += "⚠️ <b>Возможна аллергия или кожное заболевание.</b>\n"
        response += "• Проверьте на блох и клещей\n• Исключите новые продукты\n• Консультация дерматолога\n\n"
    else:
        response += "ℹ️ <b>Общие рекомендации:</b>\n"
        response += "• Наблюдайте за состоянием\n• Измерьте температуру\n• При ухудшении - обратитесь к ветеринару\n\n"

    response += f"<b>📝 Ваши симптомы сохранены:</b>\n{symptoms_text}\n\n"
    response += "<b>⚠️ ВНИМАНИЕ:</b> Это только рекомендации. Для точного диагноза обратитесь к ветеринару!"

    await state.clear()

    await message.answer(
        response,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📍 Найти клинику", callback_data="menu_clinics")],
                [InlineKeyboardButton(text="💬 Чат с ветер.", callback_data="menu_vet_chat")],
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")],
            ]
        ),
    )

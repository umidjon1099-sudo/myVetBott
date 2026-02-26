"""Обработчики раздела профиля: создание, просмотр и очистка профилей."""
from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from data_store import user_profiles, vet_profiles
from keyboards import get_profile_menu
from handlers.common import add_to_history, get_text, safe_edit_message, tr
from handlers.start_button import back_to_main_menu
from handlers.states import ProfileStates, VetProfileStates

LOCAL = {
    "owner_create": {"ru": "👤 <b>Создание профиля владельца</b>", "en": "👤 <b>Create Owner Profile</b>", "uz": "👤 <b>Ega profilini yaratish</b>"},
    "cancel": {"ru": "❌ Отмена", "en": "❌ Cancel", "uz": "❌ Bekor qilish"},
    "owner_created": {"ru": "✅ <b>Профиль владельца успешно создан!</b>", "en": "✅ <b>Owner profile created successfully!</b>", "uz": "✅ <b>Ega profili muvaffaqiyatli yaratildi!</b>"},
    "vet_create": {"ru": "👨‍⚕️ <b>Создание профиля ветеринара</b>\n\nВведите ФИО:", "en": "👨‍⚕️ <b>Create Veterinarian Profile</b>\n\nEnter full name:", "uz": "👨‍⚕️ <b>Veterinar profilini yaratish</b>\n\nF.I.O kiriting:"},
    "vet_phone": {"ru": "📞 Введите номер телефона:", "en": "📞 Enter phone number:", "uz": "📞 Telefon raqamini kiriting:"},
    "vet_city": {"ru": "🏙 Введите город:", "en": "🏙 Enter city:", "uz": "🏙 Shaharni kiriting:"},
    "vet_spec": {"ru": "🩺 Введите специализацию:", "en": "🩺 Enter specialization:", "uz": "🩺 Mutaxassislikni kiriting:"},
    "vet_exp": {"ru": "📅 Введите опыт работы:", "en": "📅 Enter work experience:", "uz": "📅 Ish tajribasini kiriting:"},
    "vet_edu": {"ru": "🎓 Введите образование:", "en": "🎓 Enter education:", "uz": "🎓 Ta'limni kiriting:"},
    "vet_tg": {"ru": "💬 Введите Telegram username:", "en": "💬 Enter Telegram username:", "uz": "💬 Telegram username kiriting:"},
    "vet_price": {"ru": "💰 Введите стоимость консультации:", "en": "💰 Enter consultation price:", "uz": "💰 Konsultatsiya narxini kiriting:"},
    "vet_info": {"ru": "📝 Дополнительная информация:", "en": "📝 Additional information:", "uz": "📝 Qo'shimcha ma'lumot:"},
    "vet_created": {"ru": "✅ <b>Профиль ветеринара успешно создан!</b>", "en": "✅ <b>Vet profile created successfully!</b>", "uz": "✅ <b>Veterinar profili muvaffaqiyatli yaratildi!</b>"},
    "owner_view_title": {"ru": "👤 <b>Профиль владельца</b>", "en": "👤 <b>Owner Profile</b>", "uz": "👤 <b>Ega profili</b>"},
    "name": {"ru": "Имя", "en": "Name", "uz": "Ism"},
    "phone": {"ru": "Телефон", "en": "Phone", "uz": "Telefon"},
    "city": {"ru": "Город", "en": "City", "uz": "Shahar"},
    "pet": {"ru": "Питомец", "en": "Pet", "uz": "Uy hayvoni"},
    "type": {"ru": "Тип", "en": "Type", "uz": "Turi"},
    "vet_view_title": {"ru": "👨‍⚕️ <b>Профиль ветеринара</b>", "en": "👨‍⚕️ <b>Veterinarian Profile</b>", "uz": "👨‍⚕️ <b>Veterinar profili</b>"},
    "fio": {"ru": "ФИО", "en": "Full name", "uz": "F.I.O"},
    "spec": {"ru": "Специализация", "en": "Specialization", "uz": "Mutaxassislik"},
    "exp": {"ru": "Опыт", "en": "Experience", "uz": "Tajriba"},
    "price": {"ru": "Цена", "en": "Price", "uz": "Narx"},
    "profile_cleared": {"ru": "✅ Профиль очищен!", "en": "✅ Profile cleared!", "uz": "✅ Profil tozalandi!"},
    "history_owner": {"ru": "👤 Создан профиль владельца", "en": "👤 Owner profile created", "uz": "👤 Ega profili yaratildi"},
    "history_vet": {"ru": "👨‍⚕️ Создан профиль ветеринара", "en": "👨‍⚕️ Vet profile created", "uz": "👨‍⚕️ Veterinar profili yaratildi"},
    "history_clear": {"ru": "🗑️ Профили очищены", "en": "🗑️ Profiles cleared", "uz": "🗑️ Profillar tozalandi"},
}


@dp.callback_query(F.data == "menu_profile")
async def profile_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "profile_section"),
        reply_markup=get_profile_menu(user_id),
    )
    await callback.answer()


@dp.callback_query(F.data == "create_profile")
async def start_create_profile(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.set_state(ProfileStates.waiting_for_owner_name)

    await safe_edit_message(
        callback.message,
        f"{tr(user_id, LOCAL['owner_create'])}\n\n{get_text(user_id, 'enter_owner_name')}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(user_id, LOCAL["cancel"]), callback_data="menu_profile")]]
        ),
    )
    await callback.answer()


@dp.message(ProfileStates.waiting_for_owner_name)
async def process_owner_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(owner_name=message.text)
    await state.set_state(ProfileStates.waiting_for_owner_phone)

    await message.answer(
        get_text(user_id, "enter_owner_phone"),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(user_id, LOCAL["cancel"]), callback_data="menu_profile")]]
        ),
    )


@dp.message(ProfileStates.waiting_for_owner_phone)
async def process_owner_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(owner_phone=message.text)
    await state.set_state(ProfileStates.waiting_for_city)

    await message.answer(
        get_text(user_id, "enter_city"),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(user_id, LOCAL["cancel"]), callback_data="menu_profile")]]
        ),
    )


@dp.message(ProfileStates.waiting_for_city)
async def process_city(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(city=message.text)
    await state.set_state(ProfileStates.waiting_for_pet_name)

    await message.answer(
        get_text(user_id, "enter_pet_name"),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(user_id, LOCAL["cancel"]), callback_data="menu_profile")]]
        ),
    )


@dp.message(ProfileStates.waiting_for_pet_name)
async def process_pet_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(pet_name=message.text)
    await state.set_state(ProfileStates.waiting_for_pet_type)

    await message.answer(
        get_text(user_id, "enter_pet_type"),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(user_id, LOCAL["cancel"]), callback_data="menu_profile")]]
        ),
    )


@dp.message(ProfileStates.waiting_for_pet_type)
async def process_pet_type(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()

    profile_data = {
        "owner_name": data.get("owner_name"),
        "owner_phone": data.get("owner_phone"),
        "city": data.get("city"),
        "pet_name": data.get("pet_name"),
        "pet_type": message.text,
    }

    user_profiles[user_id] = profile_data
    await state.clear()
    add_to_history(user_id, f"{tr(user_id, LOCAL['history_owner'])}: {profile_data['pet_name']}")

    await message.answer(
        tr(user_id, LOCAL["owner_created"]),
        reply_markup=get_profile_menu(user_id),
    )


@dp.callback_query(F.data == "create_vet_profile")
async def start_create_vet_profile(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(VetProfileStates.waiting_for_vet_name)

    await safe_edit_message(
        callback.message,
        tr(callback.from_user.id, LOCAL["vet_create"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(callback.from_user.id, LOCAL["cancel"]), callback_data="menu_profile")]]
        ),
    )
    await callback.answer()


@dp.message(VetProfileStates.waiting_for_vet_name)
async def process_vet_name(message: types.Message, state: FSMContext):
    await state.update_data(vet_name=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_phone)
    await message.answer(
        tr(message.from_user.id, LOCAL["vet_phone"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(message.from_user.id, LOCAL["cancel"]), callback_data="menu_profile")]]
        ),
    )


@dp.message(VetProfileStates.waiting_for_vet_phone)
async def process_vet_phone(message: types.Message, state: FSMContext):
    await state.update_data(vet_phone=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_city)
    await message.answer(
        tr(message.from_user.id, LOCAL["vet_city"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(message.from_user.id, LOCAL["cancel"]), callback_data="menu_profile")]]
        ),
    )


@dp.message(VetProfileStates.waiting_for_vet_city)
async def process_vet_city(message: types.Message, state: FSMContext):
    await state.update_data(vet_city=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_specialization)
    await message.answer(
        tr(message.from_user.id, LOCAL["vet_spec"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(message.from_user.id, LOCAL["cancel"]), callback_data="menu_profile")]]
        ),
    )


@dp.message(VetProfileStates.waiting_for_vet_specialization)
async def process_vet_specialization(message: types.Message, state: FSMContext):
    await state.update_data(vet_specialization=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_experience)
    await message.answer(
        tr(message.from_user.id, LOCAL["vet_exp"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(message.from_user.id, LOCAL["cancel"]), callback_data="menu_profile")]]
        ),
    )


@dp.message(VetProfileStates.waiting_for_vet_experience)
async def process_vet_experience(message: types.Message, state: FSMContext):
    await state.update_data(vet_experience=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_education)
    await message.answer(
        tr(message.from_user.id, LOCAL["vet_edu"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(message.from_user.id, LOCAL["cancel"]), callback_data="menu_profile")]]
        ),
    )


@dp.message(VetProfileStates.waiting_for_vet_education)
async def process_vet_education(message: types.Message, state: FSMContext):
    await state.update_data(vet_education=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_telegram)
    await message.answer(
        tr(message.from_user.id, LOCAL["vet_tg"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(message.from_user.id, LOCAL["cancel"]), callback_data="menu_profile")]]
        ),
    )


@dp.message(VetProfileStates.waiting_for_vet_telegram)
async def process_vet_telegram(message: types.Message, state: FSMContext):
    await state.update_data(vet_telegram=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_consultation_price)
    await message.answer(
        tr(message.from_user.id, LOCAL["vet_price"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(message.from_user.id, LOCAL["cancel"]), callback_data="menu_profile")]]
        ),
    )


@dp.message(VetProfileStates.waiting_for_vet_consultation_price)
async def process_vet_consultation_price(message: types.Message, state: FSMContext):
    await state.update_data(vet_consultation_price=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_info)
    await message.answer(
        tr(message.from_user.id, LOCAL["vet_info"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=tr(message.from_user.id, LOCAL["cancel"]), callback_data="menu_profile")]]
        ),
    )


@dp.message(VetProfileStates.waiting_for_vet_info)
async def process_vet_info(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()

    vet_profiles[user_id] = {
        "vet_name": data.get("vet_name"),
        "vet_phone": data.get("vet_phone"),
        "vet_city": data.get("vet_city"),
        "vet_specialization": data.get("vet_specialization"),
        "vet_experience": data.get("vet_experience"),
        "vet_education": data.get("vet_education"),
        "vet_telegram": data.get("vet_telegram"),
        "vet_consultation_price": data.get("vet_consultation_price"),
        "vet_info": message.text,
    }

    await state.clear()
    add_to_history(user_id, tr(user_id, LOCAL["history_vet"]))

    await message.answer(
        tr(user_id, LOCAL["vet_created"]),
        reply_markup=get_profile_menu(user_id),
    )


@dp.callback_query(F.data == "profile_view")
async def view_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    profile = user_profiles.get(user_id)

    if not profile:
        text = get_text(user_id, "profile_empty")
    else:
        text = (
            f"{tr(user_id, LOCAL['owner_view_title'])}\n\n"
            f"<b>{tr(user_id, LOCAL['name'])}:</b> {profile.get('owner_name', '-') }\n"
            f"<b>{tr(user_id, LOCAL['phone'])}:</b> {profile.get('owner_phone', '-') }\n"
            f"<b>{tr(user_id, LOCAL['city'])}:</b> {profile.get('city', '-') }\n"
            f"<b>{tr(user_id, LOCAL['pet'])}:</b> {profile.get('pet_name', '-') }\n"
            f"<b>{tr(user_id, LOCAL['type'])}:</b> {profile.get('pet_type', '-') }"
        )

    await safe_edit_message(callback.message, text, reply_markup=get_profile_menu(user_id))
    await callback.answer()


@dp.callback_query(F.data == "vet_profile_view")
async def view_vet_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    profile = vet_profiles.get(user_id)

    if not profile:
        text = get_text(user_id, "vet_profile_empty")
    else:
        text = (
            f"{tr(user_id, LOCAL['vet_view_title'])}\n\n"
            f"<b>{tr(user_id, LOCAL['fio'])}:</b> {profile.get('vet_name', '-') }\n"
            f"<b>{tr(user_id, LOCAL['phone'])}:</b> {profile.get('vet_phone', '-') }\n"
            f"<b>{tr(user_id, LOCAL['city'])}:</b> {profile.get('vet_city', '-') }\n"
            f"<b>{tr(user_id, LOCAL['spec'])}:</b> {profile.get('vet_specialization', '-') }\n"
            f"<b>{tr(user_id, LOCAL['exp'])}:</b> {profile.get('vet_experience', '-') }\n"
            f"<b>{tr(user_id, LOCAL['price'])}:</b> {profile.get('vet_consultation_price', '-') }"
        )

    await safe_edit_message(callback.message, text, reply_markup=get_profile_menu(user_id))
    await callback.answer()


@dp.callback_query(F.data == "profile_clear")
async def clear_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_profiles.pop(user_id, None)
    vet_profiles.pop(user_id, None)

    add_to_history(user_id, tr(user_id, LOCAL["history_clear"]))
    await callback.answer(tr(user_id, LOCAL["profile_cleared"]))
    await back_to_main_menu(callback)

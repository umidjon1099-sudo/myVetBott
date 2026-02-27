"""Обработчики раздела профиля: создание, просмотр и редактирование анкет."""
from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from bot_config import dp
from bot_data import UZBEK_CITIES
from data_store import user_languages, user_profiles, vet_profiles
from keyboards import get_profile_menu
from handlers.common import add_to_history, get_text, safe_edit_message, tr
from handlers.start_button import back_to_main_menu
from handlers.states import ProfileStates, VetProfileStates

LOCAL = {
    "create_menu_title": {
        "ru": "✍️ <b>Создать профиль</b>\n\nВыберите тип анкеты:",
        "en": "✍️ <b>Create Profile</b>\n\nChoose profile type:",
        "uz": "✍️ <b>Profil yaratish</b>\n\nAnketa turini tanlang:",
    },
    "view_menu_title": {
        "ru": "👁️ <b>Посмотреть профиль</b>\n\nВыберите действие:",
        "en": "👁️ <b>View Profile</b>\n\nChoose action:",
        "uz": "👁️ <b>Profilni ko'rish</b>\n\nAmalni tanlang:",
    },
    "edit_menu_title": {
        "ru": "🛠️ <b>Редактировать профиль</b>\n\nЧто хотите изменить?",
        "en": "🛠️ <b>Edit Profile</b>\n\nWhat do you want to edit?",
        "uz": "🛠️ <b>Profilni tahrirlash</b>\n\nNimani o'zgartirmoqchisiz?",
    },
    "create_pet_btn": {"ru": "🐾 Создать профиль питомца", "en": "🐾 Create pet profile", "uz": "🐾 Uy hayvoni profilini yaratish"},
    "create_vet_btn": {"ru": "👨‍⚕️ Создать профиль ветеринара", "en": "👨‍⚕️ Create vet profile", "uz": "👨‍⚕️ Veterinar profilini yaratish"},
    "view_pet_btn": {"ru": "🐾 Посмотреть анкету питомца", "en": "🐾 View pet profile", "uz": "🐾 Uy hayvoni anketasini ko'rish"},
    "view_vet_btn": {"ru": "👨‍⚕️ Посмотреть профиль вет.", "en": "👨‍⚕️ View vet profile", "uz": "👨‍⚕️ Veterinar profilini ko'rish"},
    "edit_main_btn": {"ru": "🛠️ Редактировать профиль", "en": "🛠️ Edit profile", "uz": "🛠️ Profilni tahrirlash"},
    "edit_pet_btn": {"ru": "🐾 Редактировать профиль питомца", "en": "🐾 Edit pet profile", "uz": "🐾 Uy hayvoni profilini tahrirlash"},
    "edit_vet_btn": {"ru": "👨‍⚕️ Редактировать профиль вет.", "en": "👨‍⚕️ Edit vet profile", "uz": "👨‍⚕️ Veterinar profilini tahrirlash"},
    "back": {"ru": "🔙 Назад", "en": "🔙 Back", "uz": "🔙 Orqaga"},
    "main_menu": {"ru": "🏠 Главное меню", "en": "🏠 Main Menu", "uz": "🏠 Asosiy menyu"},
    "owner_create": {"ru": "👤 <b>Создание анкеты питомца</b>", "en": "👤 <b>Create pet profile</b>", "uz": "👤 <b>Uy hayvoni anketasini yaratish</b>"},
    "owner_edit": {"ru": "👤 <b>Редактирование анкеты питомца</b>", "en": "👤 <b>Edit pet profile</b>", "uz": "👤 <b>Uy hayvoni anketasini tahrirlash</b>"},
    "cancel": {"ru": "❌ Отмена", "en": "❌ Cancel", "uz": "❌ Bekor qilish"},
    "pet_photo": {"ru": "📸 Отправьте фото питомца:", "en": "📸 Send pet photo:", "uz": "📸 Uy hayvoni rasmini yuboring:"},
    "photo_only": {"ru": "❌ Пожалуйста, отправьте фото.", "en": "❌ Please send a photo.", "uz": "❌ Iltimos, rasm yuboring."},
    "owner_created": {"ru": "✅ <b>Профиль питомца успешно сохранён!</b>", "en": "✅ <b>Pet profile saved!</b>", "uz": "✅ <b>Uy hayvoni profili saqlandi!</b>"},
    "vet_create": {"ru": "👨‍⚕️ <b>Создание CV ветеринара</b>\n\nВведите ФИО:", "en": "👨‍⚕️ <b>Create Vet CV</b>\n\nEnter full name:", "uz": "👨‍⚕️ <b>Veterinar CV yaratish</b>\n\nF.I.O kiriting:"},
    "vet_edit": {"ru": "👨‍⚕️ <b>Редактирование CV ветеринара</b>\n\nВведите ФИО:", "en": "👨‍⚕️ <b>Edit Vet CV</b>\n\nEnter full name:", "uz": "👨‍⚕️ <b>Veterinar CV tahriri</b>\n\nF.I.O kiriting:"},
    "vet_phone": {"ru": "📞 Введите номер телефона:", "en": "📞 Enter phone number:", "uz": "📞 Telefon raqamini kiriting:"},
    "vet_city": {"ru": "🏙 Введите город:", "en": "🏙 Enter city:", "uz": "🏙 Shaharni kiriting:"},
    "vet_spec": {"ru": "🩺 Введите специализацию:", "en": "🩺 Enter specialization:", "uz": "🩺 Mutaxassislikni kiriting:"},
    "vet_exp": {"ru": "📅 Введите опыт работы:", "en": "📅 Enter work experience:", "uz": "📅 Ish tajribasini kiriting:"},
    "vet_edu": {"ru": "🎓 Введите образование:", "en": "🎓 Enter education:", "uz": "🎓 Ta'limni kiriting:"},
    "vet_tg": {"ru": "💬 Введите Telegram username:", "en": "💬 Enter Telegram username:", "uz": "💬 Telegram username kiriting:"},
    "vet_price": {"ru": "💰 Введите стоимость консультации:", "en": "💰 Enter consultation price:", "uz": "💰 Konsultatsiya narxini kiriting:"},
    "vet_info": {"ru": "📝 Дополнительная информация:", "en": "📝 Additional information:", "uz": "📝 Qo'shimcha ma'lumot:"},
    "send_vet_photo": {"ru": "📸 Отправьте фото для CV:", "en": "📸 Send photo for CV:", "uz": "📸 CV uchun rasm yuboring:"},
    "vet_created": {"ru": "✅ <b>Профиль ветеринара успешно сохранён!</b>", "en": "✅ <b>Vet profile saved!</b>", "uz": "✅ <b>Veterinar profili saqlandi!</b>"},
    "owner_view_title": {"ru": "🐾 <b>Анкета питомца</b>", "en": "🐾 <b>Pet Profile</b>", "uz": "🐾 <b>Uy hayvoni anketasi</b>"},
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
    "vet_info_label": {"ru": "О себе", "en": "About", "uz": "O'zi haqida"},
    "profile_cleared": {"ru": "✅ Профили очищены!", "en": "✅ Profiles cleared!", "uz": "✅ Profillar tozalandi!"},
    "history_owner": {"ru": "👤 Сохранена анкета питомца", "en": "👤 Pet profile saved", "uz": "👤 Uy hayvoni anketasi saqlandi"},
    "history_vet": {"ru": "👨‍⚕️ Сохранён профиль ветеринара", "en": "👨‍⚕️ Vet profile saved", "uz": "👨‍⚕️ Veterinar profili saqlandi"},
    "history_clear": {"ru": "🗑️ Профили очищены", "en": "🗑️ Profiles cleared", "uz": "🗑️ Profillar tozalandi"},
    "share_phone_btn": {"ru": "📲 Отправить мой номер", "en": "📲 Share my number", "uz": "📲 Raqamimni yuborish"},
    "manual_input_btn": {"ru": "✍️ Ввести вручную", "en": "✍️ Enter manually", "uz": "✍️ Qo'lda kiritish"},
    "choose_city": {"ru": "🌍 Выберите город:", "en": "🌍 Choose city:", "uz": "🌍 Shaharni tanlang:"},
    "city_manual_btn": {"ru": "✍️ Ввести город вручную", "en": "✍️ Enter city manually", "uz": "✍️ Shaharni qo'lda kiritish"},
    "city_manual_prompt": {"ru": "🌍 Введите город вручную:", "en": "🌍 Enter city manually:", "uz": "🌍 Shaharni qo'lda kiriting:"},
    "pet_type_choose": {"ru": "🐾 Выберите вид животного:", "en": "🐾 Choose pet type:", "uz": "🐾 Hayvon turini tanlang:"},
    "vet_spec_choose": {"ru": "🩺 Выберите специализацию:", "en": "🩺 Choose specialization:", "uz": "🩺 Mutaxassislikni tanlang:"},
    "manual_type_prompt": {"ru": "✍️ Введите вид животного вручную:", "en": "✍️ Enter pet type manually:", "uz": "✍️ Hayvon turini qo'lda kiriting:"},
    "manual_spec_prompt": {"ru": "✍️ Введите специализацию вручную:", "en": "✍️ Enter specialization manually:", "uz": "✍️ Mutaxassislikni qo'lda kiriting:"},
    "pet_type_manual": {"ru": "✍️ Ввести вид вручную", "en": "✍️ Enter type manually", "uz": "✍️ Turni qo'lda kiritish"},
    "spec_manual": {"ru": "✍️ Ввести вручную", "en": "✍️ Enter manually", "uz": "✍️ Qo'lda kiritish"},
    "pet_breed_prompt": {"ru": "🏷️ Введите породу:", "en": "🏷️ Enter breed:", "uz": "🏷️ Zotini kiriting:"},
    "pet_age_prompt": {"ru": "🎂 Введите возраст:", "en": "🎂 Enter age:", "uz": "🎂 Yoshini kiriting:"},
    "pet_weight_prompt": {"ru": "⚖️ Введите вес:", "en": "⚖️ Enter weight:", "uz": "⚖️ Vaznini kiriting:"},
    "pet_color_prompt": {"ru": "🎨 Введите цвет:", "en": "🎨 Enter color:", "uz": "🎨 Rangini kiriting:"},
    "pet_allergies_prompt": {"ru": "⚠️ Укажите аллергии:", "en": "⚠️ Enter allergies:", "uz": "⚠️ Allergiyalarni kiriting:"},
    "pet_diseases_prompt": {"ru": "🏥 Укажите болезни:", "en": "🏥 Enter diseases:", "uz": "🏥 Kasalliklarni kiriting:"},
    "pet_vaccines_prompt": {"ru": "💉 Укажите вакцинации:", "en": "💉 Enter vaccinations:", "uz": "💉 Emlashlarni kiriting:"},
    "profile_title": {"ru": "👤 ВАШ ПРОФИЛЬ", "en": "👤 YOUR PROFILE", "uz": "👤 SIZNING PROFILINGIZ"},
    "owner_label": {"ru": "👨 Владелец", "en": "👨 Owner", "uz": "👨 Egasi"},
    "phone_label": {"ru": "📞 Телефон", "en": "📞 Phone", "uz": "📞 Telefon"},
    "city_label": {"ru": "🌍 Город", "en": "🌍 City", "uz": "🌍 Shahar"},
    "pet_label": {"ru": "🐾 Питомец", "en": "🐾 Pet", "uz": "🐾 Uy hayvoni"},
    "type_label": {"ru": "📋 Вид", "en": "📋 Type", "uz": "📋 Turi"},
    "breed_label": {"ru": "🏷️ Порода", "en": "🏷️ Breed", "uz": "🏷️ Zoti"},
    "age_label": {"ru": "🎂 Возраст", "en": "🎂 Age", "uz": "🎂 Yoshi"},
    "weight_label": {"ru": "⚖️ Вес", "en": "⚖️ Weight", "uz": "⚖️ Vazni"},
    "color_label": {"ru": "🎨 Цвет", "en": "🎨 Color", "uz": "🎨 Rangi"},
    "allergies_label": {"ru": "⚠️ Аллергии", "en": "⚠️ Allergies", "uz": "⚠️ Allergiyalar"},
    "diseases_label": {"ru": "🏥 Болезни", "en": "🏥 Diseases", "uz": "🏥 Kasalliklar"},
    "vaccines_label": {"ru": "💉 Вакцинации", "en": "💉 Vaccinations", "uz": "💉 Emlashlar"},
}

PET_TYPE_OPTIONS = [
    {"id": "dog", "ru": "🐕 Собака", "en": "🐕 Dog", "uz": "🐕 It"},
    {"id": "cat", "ru": "🐱 Кошка", "en": "🐱 Cat", "uz": "🐱 Mushuk"},
    {"id": "bird", "ru": "🐦 Птица", "en": "🐦 Bird", "uz": "🐦 Qush"},
    {"id": "rodent", "ru": "🐹 Грызун", "en": "🐹 Rodent", "uz": "🐹 Kemiruvchi"},
    {"id": "fish", "ru": "🐠 Рыбка", "en": "🐠 Fish", "uz": "🐠 Baliq"},
]

VET_SPEC_OPTIONS = [
    {"id": "therapist", "ru": "Ветеринарный терапевт", "en": "Veterinary Therapist", "uz": "Veterinar terapevt"},
    {"id": "surgeon", "ru": "Ветеринарный хирург", "en": "Veterinary Surgeon", "uz": "Veterinar jarroh"},
    {"id": "dermatologist", "ru": "Дерматолог", "en": "Dermatologist", "uz": "Dermatolog"},
    {"id": "cardiologist", "ru": "Кардиолог", "en": "Cardiologist", "uz": "Kardiolog"},
    {"id": "neurologist", "ru": "Невролог", "en": "Neurologist", "uz": "Nevrolog"},
    {"id": "exotic", "ru": "Экзотические животные", "en": "Exotic Animals", "uz": "Ekzotik hayvonlar"},
]


def _cancel_kb(user_id: int, back_cb: str = "menu_profile") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data=back_cb)],
            [InlineKeyboardButton(text=tr(user_id, LOCAL["main_menu"]), callback_data="back_to_menu")],
        ]
    )


def _view_kb(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="profile_view_menu")],
            [InlineKeyboardButton(text=tr(user_id, LOCAL["main_menu"]), callback_data="back_to_menu")],
        ]
    )


def _contact_kb(user_id: int) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=tr(user_id, LOCAL["share_phone_btn"]), request_contact=True)],
            [KeyboardButton(text=tr(user_id, LOCAL["manual_input_btn"]))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def _pet_type_kb(user_id: int, back_cb: str = "menu_profile") -> InlineKeyboardMarkup:
    lang = user_languages.get(user_id, "ru")
    rows = [[InlineKeyboardButton(text=item.get(lang, item["ru"]), callback_data=f"pet_type_{item['id']}")] for item in PET_TYPE_OPTIONS]
    rows.append([InlineKeyboardButton(text=tr(user_id, LOCAL["pet_type_manual"]), callback_data="pet_type_manual")])
    rows.append([InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data=back_cb)])
    rows.append([InlineKeyboardButton(text=tr(user_id, LOCAL["main_menu"]), callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _vet_spec_kb(user_id: int, back_cb: str = "menu_profile") -> InlineKeyboardMarkup:
    lang = user_languages.get(user_id, "ru")
    rows = [[InlineKeyboardButton(text=item.get(lang, item["ru"]), callback_data=f"vet_spec_{item['id']}")] for item in VET_SPEC_OPTIONS]
    rows.append([InlineKeyboardButton(text=tr(user_id, LOCAL["spec_manual"]), callback_data="vet_spec_manual")])
    rows.append([InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data=back_cb)])
    rows.append([InlineKeyboardButton(text=tr(user_id, LOCAL["main_menu"]), callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _city_kb(user_id: int, prefix: str, back_cb: str) -> InlineKeyboardMarkup:
    rows = []
    row = []
    for city_key in UZBEK_CITIES:
        row.append(InlineKeyboardButton(text=get_text(user_id, city_key), callback_data=f"{prefix}_{city_key}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton(text=tr(user_id, LOCAL["city_manual_btn"]), callback_data=f"{prefix}_manual")])
    rows.append([InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data=back_cb)])
    rows.append([InlineKeyboardButton(text=tr(user_id, LOCAL["main_menu"]), callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _pet_profile_text(user_id: int, profile: dict) -> str:
    return (
        f"{tr(user_id, LOCAL['profile_title'])}\n"
        f"════════════════════\n"
        f"{tr(user_id, LOCAL['owner_label'])}: {profile.get('owner_name', '-') }\n"
        f"{tr(user_id, LOCAL['phone_label'])}: {profile.get('owner_phone', '-') }\n"
        f"{tr(user_id, LOCAL['city_label'])}: {profile.get('city', '-') }\n\n"
        f"{tr(user_id, LOCAL['pet_label'])}: {profile.get('pet_name', '-') }\n"
        f"{tr(user_id, LOCAL['type_label'])}: {profile.get('pet_type', '-') }\n"
        f"{tr(user_id, LOCAL['breed_label'])}: {profile.get('pet_breed', '-') }\n"
        f"{tr(user_id, LOCAL['age_label'])}: {profile.get('pet_age', '-') }\n"
        f"{tr(user_id, LOCAL['weight_label'])}: {profile.get('pet_weight', '-') }\n"
        f"{tr(user_id, LOCAL['color_label'])}: {profile.get('pet_color', '-') }\n\n"
        f"{tr(user_id, LOCAL['allergies_label'])}: {profile.get('allergies', '-') }\n"
        f"{tr(user_id, LOCAL['diseases_label'])}: {profile.get('diseases', '-') }\n"
        f"{tr(user_id, LOCAL['vaccines_label'])}: {profile.get('vaccinations', '-') }\n"
        f"════════════════════"
    )


def _vet_profile_text(user_id: int, profile: dict) -> str:
    return (
        f"{tr(user_id, LOCAL['vet_view_title'])}\n\n"
        f"<b>{tr(user_id, LOCAL['fio'])}:</b> {profile.get('vet_name', '-') }\n"
        f"<b>{tr(user_id, LOCAL['phone'])}:</b> {profile.get('vet_phone', '-') }\n"
        f"<b>{tr(user_id, LOCAL['city'])}:</b> {profile.get('vet_city', '-') }\n"
        f"<b>{tr(user_id, LOCAL['spec'])}:</b> {profile.get('vet_specialization', '-') }\n"
        f"<b>{tr(user_id, LOCAL['exp'])}:</b> {profile.get('vet_experience', '-') }\n"
        f"<b>{tr(user_id, LOCAL['price'])}:</b> {profile.get('vet_consultation_price', '-') }\n"
        f"<b>{tr(user_id, LOCAL['vet_info_label'])}:</b> {profile.get('vet_info', '-') }"
    )


@dp.callback_query(F.data == "menu_profile")
async def profile_menu(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.clear()
    await safe_edit_message(
        callback.message,
        get_text(user_id, "profile_section"),
        reply_markup=get_profile_menu(user_id),
    )
    await callback.answer()


@dp.callback_query(F.data == "profile_create_menu")
async def profile_create_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        tr(user_id, LOCAL["create_menu_title"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["create_pet_btn"]), callback_data="create_profile")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["create_vet_btn"]), callback_data="create_vet_profile")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="menu_profile")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["main_menu"]), callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()


@dp.callback_query(F.data == "profile_view_menu")
async def profile_view_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        tr(user_id, LOCAL["view_menu_title"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["view_pet_btn"]), callback_data="profile_view")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["view_vet_btn"]), callback_data="vet_profile_view")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["edit_main_btn"]), callback_data="profile_edit_menu")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="menu_profile")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["main_menu"]), callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()


@dp.callback_query(F.data == "profile_edit_menu")
async def profile_edit_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        tr(user_id, LOCAL["edit_menu_title"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["edit_pet_btn"]), callback_data="edit_pet_profile")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["edit_vet_btn"]), callback_data="edit_vet_profile")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="profile_view_menu")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["main_menu"]), callback_data="back_to_menu")],
            ]
        ),
    )
    await callback.answer()


@dp.callback_query(F.data == "create_profile")
async def start_create_profile(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.set_state(ProfileStates.waiting_for_owner_name)
    await state.update_data(profile_back_cb="profile_create_menu")
    await safe_edit_message(
        callback.message,
        f"{tr(user_id, LOCAL['owner_create'])}\n\n{get_text(user_id, 'enter_owner_name')}",
        reply_markup=_cancel_kb(user_id, "profile_create_menu"),
    )
    await callback.answer()


@dp.callback_query(F.data == "edit_pet_profile")
async def edit_pet_profile(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.set_state(ProfileStates.waiting_for_owner_name)
    await state.update_data(profile_back_cb="profile_edit_menu")
    await safe_edit_message(
        callback.message,
        f"{tr(user_id, LOCAL['owner_edit'])}\n\n{get_text(user_id, 'enter_owner_name')}",
        reply_markup=_cancel_kb(user_id, "profile_edit_menu"),
    )
    await callback.answer()


@dp.message(ProfileStates.waiting_for_owner_name)
async def process_owner_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(owner_name=message.text)
    await state.set_state(ProfileStates.waiting_for_owner_phone)
    await message.answer(get_text(user_id, "enter_owner_phone"), reply_markup=_contact_kb(user_id))


@dp.message(ProfileStates.waiting_for_owner_phone)
async def process_owner_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    manual_label = tr(user_id, LOCAL["manual_input_btn"])
    if message.text == manual_label:
        await message.answer(get_text(user_id, "enter_owner_phone"), reply_markup=ReplyKeyboardRemove())
        return

    phone_value = message.contact.phone_number if message.contact else message.text
    await state.update_data(owner_phone=phone_value)
    await state.set_state(ProfileStates.waiting_for_city)
    data = await state.get_data()
    await message.answer("⁠", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        tr(user_id, LOCAL["choose_city"]),
        reply_markup=_city_kb(user_id, "profile_city", data.get("profile_back_cb", "menu_profile")),
    )


@dp.callback_query(ProfileStates.waiting_for_city, F.data.startswith("profile_city_"))
async def process_city_choice(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    token = callback.data.replace("profile_city_", "")
    if token == "manual":
        await state.set_state(ProfileStates.waiting_for_city_manual)
        data = await state.get_data()
        await safe_edit_message(
            callback.message,
            tr(user_id, LOCAL["city_manual_prompt"]),
            reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")),
        )
        await callback.answer()
        return

    city_name = get_text(user_id, token)
    await state.update_data(city=city_name)
    await state.set_state(ProfileStates.waiting_for_pet_name)
    data = await state.get_data()
    await safe_edit_message(
        callback.message,
        get_text(user_id, "enter_pet_name"),
        reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")),
    )
    await callback.answer()


@dp.message(ProfileStates.waiting_for_city_manual)
async def process_city_manual(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(city=message.text)
    await state.set_state(ProfileStates.waiting_for_pet_name)
    data = await state.get_data()
    await message.answer(get_text(user_id, "enter_pet_name"), reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")))


@dp.message(ProfileStates.waiting_for_city)
async def process_city_fallback(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(city=message.text)
    await state.set_state(ProfileStates.waiting_for_pet_name)
    data = await state.get_data()
    await message.answer(get_text(user_id, "enter_pet_name"), reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")))


@dp.message(ProfileStates.waiting_for_pet_name)
async def process_pet_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(pet_name=message.text)
    await state.set_state(ProfileStates.waiting_for_pet_type)
    data = await state.get_data()
    await message.answer(tr(user_id, LOCAL["pet_type_choose"]), reply_markup=_pet_type_kb(user_id, data.get("profile_back_cb", "menu_profile")))


@dp.callback_query(ProfileStates.waiting_for_pet_type, F.data.startswith("pet_type_"))
async def process_pet_type_choice(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    token = callback.data.replace("pet_type_", "")
    if token == "manual":
        await state.set_state(ProfileStates.waiting_for_pet_type_manual)
        data = await state.get_data()
        await safe_edit_message(
            callback.message,
            tr(user_id, LOCAL["manual_type_prompt"]),
            reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")),
        )
        await callback.answer()
        return

    selected = next((item for item in PET_TYPE_OPTIONS if item["id"] == token), None)
    lang = user_languages.get(user_id, "ru")
    await state.update_data(pet_type=(selected.get(lang, selected["ru"]) if selected else token))
    await state.set_state(ProfileStates.waiting_for_pet_breed)
    data = await state.get_data()
    await safe_edit_message(
        callback.message,
        tr(user_id, LOCAL["pet_breed_prompt"]),
        reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")),
    )
    await callback.answer()


@dp.message(ProfileStates.waiting_for_pet_type_manual)
async def process_pet_type_manual(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(pet_type=message.text)
    await state.set_state(ProfileStates.waiting_for_pet_breed)
    data = await state.get_data()
    await message.answer(tr(user_id, LOCAL["pet_breed_prompt"]), reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")))


@dp.message(ProfileStates.waiting_for_pet_type)
async def process_pet_type_text_fallback(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(pet_type=message.text)
    await state.set_state(ProfileStates.waiting_for_pet_breed)
    data = await state.get_data()
    await message.answer(tr(user_id, LOCAL["pet_breed_prompt"]), reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")))


@dp.message(ProfileStates.waiting_for_pet_breed)
async def process_pet_breed(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(pet_breed=message.text)
    await state.set_state(ProfileStates.waiting_for_pet_age)
    data = await state.get_data()
    await message.answer(tr(user_id, LOCAL["pet_age_prompt"]), reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")))


@dp.message(ProfileStates.waiting_for_pet_age)
async def process_pet_age(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(pet_age=message.text)
    await state.set_state(ProfileStates.waiting_for_pet_weight)
    data = await state.get_data()
    await message.answer(tr(user_id, LOCAL["pet_weight_prompt"]), reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")))


@dp.message(ProfileStates.waiting_for_pet_weight)
async def process_pet_weight(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(pet_weight=message.text)
    await state.set_state(ProfileStates.waiting_for_pet_color)
    data = await state.get_data()
    await message.answer(tr(user_id, LOCAL["pet_color_prompt"]), reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")))


@dp.message(ProfileStates.waiting_for_pet_color)
async def process_pet_color(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(pet_color=message.text)
    await state.set_state(ProfileStates.waiting_for_allergies)
    data = await state.get_data()
    await message.answer(tr(user_id, LOCAL["pet_allergies_prompt"]), reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")))


@dp.message(ProfileStates.waiting_for_allergies)
async def process_allergies(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(allergies=message.text)
    await state.set_state(ProfileStates.waiting_for_diseases)
    data = await state.get_data()
    await message.answer(tr(user_id, LOCAL["pet_diseases_prompt"]), reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")))


@dp.message(ProfileStates.waiting_for_diseases)
async def process_diseases(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(diseases=message.text)
    await state.set_state(ProfileStates.waiting_for_vaccinations)
    data = await state.get_data()
    await message.answer(tr(user_id, LOCAL["pet_vaccines_prompt"]), reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")))


@dp.message(ProfileStates.waiting_for_vaccinations)
async def process_vaccinations(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vaccinations=message.text)
    await state.set_state(ProfileStates.waiting_for_pet_photo)
    data = await state.get_data()
    await message.answer(tr(user_id, LOCAL["pet_photo"]), reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")))


@dp.message(ProfileStates.waiting_for_pet_photo)
async def process_pet_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not message.photo:
        data = await state.get_data()
        await message.answer(tr(user_id, LOCAL["photo_only"]), reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")))
        return

    data = await state.get_data()
    profile_data = {
        "owner_name": data.get("owner_name"),
        "owner_phone": data.get("owner_phone"),
        "city": data.get("city"),
        "pet_name": data.get("pet_name"),
        "pet_type": data.get("pet_type"),
        "pet_breed": data.get("pet_breed"),
        "pet_age": data.get("pet_age"),
        "pet_weight": data.get("pet_weight"),
        "pet_color": data.get("pet_color"),
        "allergies": data.get("allergies"),
        "diseases": data.get("diseases"),
        "vaccinations": data.get("vaccinations"),
        "pet_photo": message.photo[-1].file_id,
    }
    user_profiles[user_id] = profile_data
    await state.clear()
    add_to_history(user_id, f"{tr(user_id, LOCAL['history_owner'])}: {profile_data['pet_name']}")
    pretty = f"{tr(user_id, LOCAL['owner_created'])}\n\n{_pet_profile_text(user_id, profile_data)}"
    await message.answer(pretty, parse_mode="HTML", reply_markup=get_profile_menu(user_id))


@dp.callback_query(F.data == "create_vet_profile")
async def start_create_vet_profile(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(VetProfileStates.waiting_for_vet_name)
    await state.update_data(profile_back_cb="profile_create_menu")
    await safe_edit_message(
        callback.message,
        tr(callback.from_user.id, LOCAL["vet_create"]),
        reply_markup=_cancel_kb(callback.from_user.id, "profile_create_menu"),
    )
    await callback.answer()


@dp.callback_query(F.data == "edit_vet_profile")
async def edit_vet_profile(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(VetProfileStates.waiting_for_vet_name)
    await state.update_data(profile_back_cb="profile_edit_menu")
    await safe_edit_message(
        callback.message,
        tr(callback.from_user.id, LOCAL["vet_edit"]),
        reply_markup=_cancel_kb(callback.from_user.id, "profile_edit_menu"),
    )
    await callback.answer()


@dp.message(VetProfileStates.waiting_for_vet_name)
async def process_vet_name(message: types.Message, state: FSMContext):
    await state.update_data(vet_name=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_phone)
    await message.answer(tr(message.from_user.id, LOCAL["vet_phone"]), reply_markup=_contact_kb(message.from_user.id))


@dp.message(VetProfileStates.waiting_for_vet_phone)
async def process_vet_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    manual_label = tr(user_id, LOCAL["manual_input_btn"])
    if message.text == manual_label:
        await message.answer(tr(user_id, LOCAL["vet_phone"]), reply_markup=ReplyKeyboardRemove())
        return

    phone_value = message.contact.phone_number if message.contact else message.text
    await state.update_data(vet_phone=phone_value)
    await state.set_state(VetProfileStates.waiting_for_vet_city)
    data = await state.get_data()
    await message.answer("⁠", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        tr(user_id, LOCAL["choose_city"]),
        reply_markup=_city_kb(user_id, "profile_vet_city", data.get("profile_back_cb", "menu_profile")),
    )


@dp.callback_query(VetProfileStates.waiting_for_vet_city, F.data.startswith("profile_vet_city_"))
async def process_vet_city_choice(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    token = callback.data.replace("profile_vet_city_", "")
    if token == "manual":
        await state.set_state(VetProfileStates.waiting_for_vet_city_manual)
        data = await state.get_data()
        await safe_edit_message(
            callback.message,
            tr(user_id, LOCAL["city_manual_prompt"]),
            reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")),
        )
        await callback.answer()
        return

    city_name = get_text(user_id, token)
    await state.update_data(vet_city=city_name)
    await state.set_state(VetProfileStates.waiting_for_vet_specialization)
    data = await state.get_data()
    await safe_edit_message(
        callback.message,
        tr(user_id, LOCAL["vet_spec_choose"]),
        reply_markup=_vet_spec_kb(user_id, data.get("profile_back_cb", "menu_profile")),
    )
    await callback.answer()


@dp.message(VetProfileStates.waiting_for_vet_city_manual)
async def process_vet_city_manual(message: types.Message, state: FSMContext):
    await state.update_data(vet_city=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_specialization)
    data = await state.get_data()
    await message.answer(
        tr(message.from_user.id, LOCAL["vet_spec_choose"]),
        reply_markup=_vet_spec_kb(message.from_user.id, data.get("profile_back_cb", "menu_profile")),
    )


@dp.message(VetProfileStates.waiting_for_vet_city)
async def process_vet_city_fallback(message: types.Message, state: FSMContext):
    await state.update_data(vet_city=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_specialization)
    data = await state.get_data()
    await message.answer(
        tr(message.from_user.id, LOCAL["vet_spec_choose"]),
        reply_markup=_vet_spec_kb(message.from_user.id, data.get("profile_back_cb", "menu_profile")),
    )


@dp.callback_query(VetProfileStates.waiting_for_vet_specialization, F.data.startswith("vet_spec_"))
async def process_vet_specialization_choice(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    token = callback.data.replace("vet_spec_", "")
    if token == "manual":
        await state.set_state(VetProfileStates.waiting_for_vet_specialization_manual)
        data = await state.get_data()
        await safe_edit_message(
            callback.message,
            tr(user_id, LOCAL["manual_spec_prompt"]),
            reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")),
        )
        await callback.answer()
        return

    selected = next((item for item in VET_SPEC_OPTIONS if item["id"] == token), None)
    lang = user_languages.get(user_id, "ru")
    await state.update_data(vet_specialization=(selected.get(lang, selected["ru"]) if selected else token))
    await state.set_state(VetProfileStates.waiting_for_vet_experience)
    data = await state.get_data()
    await safe_edit_message(
        callback.message,
        tr(user_id, LOCAL["vet_exp"]),
        reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")),
    )
    await callback.answer()


@dp.message(VetProfileStates.waiting_for_vet_specialization_manual)
async def process_vet_specialization_manual(message: types.Message, state: FSMContext):
    await state.update_data(vet_specialization=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_experience)
    data = await state.get_data()
    await message.answer(tr(message.from_user.id, LOCAL["vet_exp"]), reply_markup=_cancel_kb(message.from_user.id, data.get("profile_back_cb", "menu_profile")))


@dp.message(VetProfileStates.waiting_for_vet_specialization)
async def process_vet_specialization_text_fallback(message: types.Message, state: FSMContext):
    await state.update_data(vet_specialization=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_experience)
    data = await state.get_data()
    await message.answer(tr(message.from_user.id, LOCAL["vet_exp"]), reply_markup=_cancel_kb(message.from_user.id, data.get("profile_back_cb", "menu_profile")))


@dp.message(VetProfileStates.waiting_for_vet_experience)
async def process_vet_experience(message: types.Message, state: FSMContext):
    await state.update_data(vet_experience=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_education)
    data = await state.get_data()
    await message.answer(tr(message.from_user.id, LOCAL["vet_edu"]), reply_markup=_cancel_kb(message.from_user.id, data.get("profile_back_cb", "menu_profile")))


@dp.message(VetProfileStates.waiting_for_vet_education)
async def process_vet_education(message: types.Message, state: FSMContext):
    await state.update_data(vet_education=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_telegram)
    data = await state.get_data()
    await message.answer(tr(message.from_user.id, LOCAL["vet_tg"]), reply_markup=_cancel_kb(message.from_user.id, data.get("profile_back_cb", "menu_profile")))


@dp.message(VetProfileStates.waiting_for_vet_telegram)
async def process_vet_telegram(message: types.Message, state: FSMContext):
    await state.update_data(vet_telegram=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_consultation_price)
    data = await state.get_data()
    await message.answer(tr(message.from_user.id, LOCAL["vet_price"]), reply_markup=_cancel_kb(message.from_user.id, data.get("profile_back_cb", "menu_profile")))


@dp.message(VetProfileStates.waiting_for_vet_consultation_price)
async def process_vet_consultation_price(message: types.Message, state: FSMContext):
    await state.update_data(vet_consultation_price=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_info)
    data = await state.get_data()
    await message.answer(tr(message.from_user.id, LOCAL["vet_info"]), reply_markup=_cancel_kb(message.from_user.id, data.get("profile_back_cb", "menu_profile")))


@dp.message(VetProfileStates.waiting_for_vet_info)
async def process_vet_info(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vet_info=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_photo)
    data = await state.get_data()
    await message.answer(tr(user_id, LOCAL["send_vet_photo"]), reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")))


@dp.message(VetProfileStates.waiting_for_vet_photo)
async def process_vet_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not message.photo:
        data = await state.get_data()
        await message.answer(tr(user_id, LOCAL["photo_only"]), reply_markup=_cancel_kb(user_id, data.get("profile_back_cb", "menu_profile")))
        return

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
        "vet_info": data.get("vet_info"),
        "vet_photo": message.photo[-1].file_id,
    }
    await state.clear()
    add_to_history(user_id, tr(user_id, LOCAL["history_vet"]))
    pretty = f"{tr(user_id, LOCAL['vet_created'])}\n\n{_vet_profile_text(user_id, vet_profiles[user_id])}"
    await message.answer(pretty, parse_mode="HTML", reply_markup=get_profile_menu(user_id))


@dp.callback_query(F.data == "profile_view")
async def view_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    profile = user_profiles.get(user_id)
    if not profile:
        text = get_text(user_id, "profile_empty")
        await safe_edit_message(callback.message, text, reply_markup=_view_kb(user_id))
        await callback.answer()
        return

    text = _pet_profile_text(user_id, profile)
    if profile.get("pet_photo"):
        await callback.message.answer_photo(photo=profile["pet_photo"], caption=text, parse_mode="HTML", reply_markup=_view_kb(user_id))
    else:
        await safe_edit_message(callback.message, text, reply_markup=_view_kb(user_id))
    await callback.answer()


@dp.callback_query(F.data == "vet_profile_view")
async def view_vet_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    profile = vet_profiles.get(user_id)
    if not profile:
        text = get_text(user_id, "vet_profile_empty")
        await safe_edit_message(callback.message, text, reply_markup=_view_kb(user_id))
        await callback.answer()
        return

    text = _vet_profile_text(user_id, profile)
    if profile.get("vet_photo"):
        await callback.message.answer_photo(photo=profile["vet_photo"], caption=text, parse_mode="HTML", reply_markup=_view_kb(user_id))
    else:
        await safe_edit_message(callback.message, text, reply_markup=_view_kb(user_id))
    await callback.answer()


@dp.callback_query(F.data == "profile_clear")
async def clear_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_profiles.pop(user_id, None)
    vet_profiles.pop(user_id, None)
    add_to_history(user_id, tr(user_id, LOCAL["history_clear"]))
    await callback.answer(tr(user_id, LOCAL["profile_cleared"]))
    await back_to_main_menu(callback)

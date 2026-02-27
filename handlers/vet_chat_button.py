"""Обработчики раздела чата с ветеринаром и выбора направления."""
from aiogram import F, types
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from data_store import user_languages, vet_profiles
from handlers.common import safe_edit_message, tr

VETS_PER_PAGE = 6
DIRECTIONS_PER_PAGE = 8

DIRECTIONS = [
    {"ru": "Ветеринарный терапевт", "en": "Veterinary Therapist", "uz": "Veterinar terapevt"},
    {"ru": "Ветеринарный хирург", "en": "Veterinary Surgeon", "uz": "Veterinar jarroh"},
    {"ru": "Экстренная ветеринария", "en": "Emergency Veterinary Care", "uz": "Shoshilinch veterinariya"},
    {"ru": "Реаниматолог (интенсивная терапия)", "en": "Intensive Care Specialist", "uz": "Reanimatolog (intensiv terapiya)"},
    {"ru": "Анестезиолог", "en": "Anesthesiologist", "uz": "Anesteziolog"},
    {"ru": "Ортопед", "en": "Orthopedist", "uz": "Ortoped"},
    {"ru": "Травматолог", "en": "Traumatologist", "uz": "Travmatolog"},
    {"ru": "Невролог", "en": "Neurologist", "uz": "Nevrolog"},
    {"ru": "Кардиолог", "en": "Cardiologist", "uz": "Kardiolog"},
    {"ru": "Пульмонолог", "en": "Pulmonologist", "uz": "Pulmonolog"},
    {"ru": "Гастроэнтеролог", "en": "Gastroenterologist", "uz": "Gastroenterolog"},
    {"ru": "Гепатолог", "en": "Hepatologist", "uz": "Gepatolog"},
    {"ru": "Нефролог", "en": "Nephrologist", "uz": "Nefrolog"},
    {"ru": "Уролог", "en": "Urologist", "uz": "Urolog"},
    {"ru": "Репродуктолог", "en": "Reproductive Specialist", "uz": "Reproduktolog"},
    {"ru": "Акушер-гинеколог", "en": "Obstetrician-Gynecologist", "uz": "Akusher-ginekolog"},
    {"ru": "Андролог", "en": "Andrologist", "uz": "Androlog"},
    {"ru": "Лабораторный диагност", "en": "Laboratory Diagnostician", "uz": "Laboratoriya diagnosti"},
    {"ru": "Клинический патолог", "en": "Clinical Pathologist", "uz": "Klinik patolog"},
    {"ru": "Патоморфолог", "en": "Pathomorphologist", "uz": "Patomorfolog"},
    {"ru": "Цитолог", "en": "Cytologist", "uz": "Sitolog"},
    {"ru": "Гистолог", "en": "Histologist", "uz": "Gistolog"},
    {"ru": "Визуальный диагност (УЗИ)", "en": "Imaging Specialist (Ultrasound)", "uz": "Vizual diagnost (UZI)"},
    {"ru": "Рентгенолог", "en": "Radiologist", "uz": "Rentgenolog"},
    {"ru": "КТ-диагност", "en": "CT Specialist", "uz": "KT diagnost"},
    {"ru": "МРТ-диагност", "en": "MRI Specialist", "uz": "MRT diagnost"},
    {"ru": "Инфекционист", "en": "Infectious Disease Specialist", "uz": "Infeksionist"},
    {"ru": "Паразитолог", "en": "Parasitologist", "uz": "Parazitolog"},
    {"ru": "Иммунолог", "en": "Immunologist", "uz": "Immunolog"},
    {"ru": "Эпидемиолог", "en": "Epidemiologist", "uz": "Epidemiolog"},
    {"ru": "Токсиколог", "en": "Toxicologist", "uz": "Toksikolog"},
    {"ru": "Эндокринолог", "en": "Endocrinologist", "uz": "Endokrinolog"},
    {"ru": "Аллерголог", "en": "Allergist", "uz": "Allergolog"},
    {"ru": "Дерматолог", "en": "Dermatologist", "uz": "Dermatolog"},
    {"ru": "Отоларинголог (ЛОР)", "en": "Otolaryngologist (ENT)", "uz": "Otolaringolog (LOR)"},
    {"ru": "Офтальмолог", "en": "Ophthalmologist", "uz": "Oftalmolog"},
    {"ru": "Диетолог", "en": "Dietitian", "uz": "Diyetolog"},
    {"ru": "Нутрициолог", "en": "Nutrition Specialist", "uz": "Nutritsiolog"},
    {"ru": "Метаболист", "en": "Metabolism Specialist", "uz": "Metabolist"},
    {"ru": "Зоопсихолог", "en": "Animal Psychologist", "uz": "Zoopsixolog"},
    {"ru": "Поведенческий ветеринар", "en": "Behavioral Veterinarian", "uz": "Xulq-atvor veterinari"},
    {"ru": "Реабилитолог", "en": "Rehabilitation Specialist", "uz": "Reabilitolog"},
    {"ru": "Физиотерапевт", "en": "Physiotherapist", "uz": "Fizioterapevt"},
    {"ru": "Ветеринар ЛФК", "en": "Veterinary Exercise Therapy Specialist", "uz": "Veterinar LFK mutaxassisi"},
    {"ru": "Ветеринар мелких домашних животных", "en": "Small Animal Veterinarian", "uz": "Mayda uy hayvonlari veterinari"},
    {"ru": "Ветеринар кошек", "en": "Feline Veterinarian", "uz": "Mushuklar veterinari"},
    {"ru": "Ветеринар собак", "en": "Canine Veterinarian", "uz": "Itlar veterinari"},
    {"ru": "Ветеринар экзотических животных", "en": "Exotic Animal Veterinarian", "uz": "Ekzotik hayvonlar veterinari"},
    {"ru": "Ветеринар птиц", "en": "Avian Veterinarian", "uz": "Qushlar veterinari"},
    {"ru": "Орнитолог", "en": "Ornithologist", "uz": "Ornitolog"},
    {"ru": "Ихтиопатолог", "en": "Ichthyopathologist", "uz": "Ixtiopatolog"},
    {"ru": "Ветеринар грызунов", "en": "Rodent Veterinarian", "uz": "Kemiruvchilar veterinari"},
    {"ru": "Ветеринар рептилий", "en": "Reptile Veterinarian", "uz": "Sudralib yuruvchilar veterinari"},
    {"ru": "Ветеринар КРС", "en": "Cattle Veterinarian", "uz": "Yirik shoxli qoramol veterinari"},
    {"ru": "Ветеринар МРС", "en": "Small Ruminant Veterinarian", "uz": "Mayda shoxli chorva veterinari"},
    {"ru": "Ветеринар свиноводства", "en": "Swine Veterinarian", "uz": "Cho'chqachilik veterinari"},
    {"ru": "Ветеринар птицеводства", "en": "Poultry Veterinarian", "uz": "Parrandachilik veterinari"},
    {"ru": "Ветеринар коневодства", "en": "Equine Veterinarian", "uz": "Otchilik veterinari"},
    {"ru": "Ветеринар верблюдоводства", "en": "Camel Husbandry Veterinarian", "uz": "Tuyachilik veterinari"},
    {"ru": "Ветеринар фермерских хозяйств", "en": "Farm Practice Veterinarian", "uz": "Fermer xo'jaliklari veterinari"},
    {"ru": "Ветеринарный микробиолог", "en": "Veterinary Microbiologist", "uz": "Veterinar mikrobiolog"},
    {"ru": "Ветеринарный вирусолог", "en": "Veterinary Virologist", "uz": "Veterinar virusolog"},
    {"ru": "Ветеринарный фармаколог", "en": "Veterinary Pharmacologist", "uz": "Veterinar farmakolog"},
    {"ru": "Ветеринарный биотехнолог", "en": "Veterinary Biotechnologist", "uz": "Veterinar biotexnolog"},
    {"ru": "Ветеринарный инспектор", "en": "Veterinary Inspector", "uz": "Veterinar inspektor"},
    {"ru": "Ветеринарный санитарный врач", "en": "Veterinary Sanitary Doctor", "uz": "Veterinar sanitariya shifokori"},
    {"ru": "Ветеринарный эксперт", "en": "Veterinary Expert", "uz": "Veterinar ekspert"},
    {"ru": "Ветеринарный эпизоотолог", "en": "Epizootologist", "uz": "Veterinar epizootolog"},
    {"ru": "Ветеринарный менеджер", "en": "Veterinary Manager", "uz": "Veterinar menejer"},
    {"ru": "Руководитель клиники", "en": "Clinic Director", "uz": "Klinika rahbari"},
    {"ru": "Преподаватель ветеринарии", "en": "Veterinary Teacher", "uz": "Veterinariya o'qituvchisi"},
    {"ru": "Научный сотрудник", "en": "Research Scientist", "uz": "Ilmiy xodim"},
]

LOCAL = {
    "title": {
        "ru": "💬 <b>Чат с ветеринаром</b>",
        "en": "💬 <b>Vet Chat</b>",
        "uz": "💬 <b>Veterinar bilan chat</b>",
    },
    "directions": {
        "ru": "🧭 Выбор ветеринара по направлению",
        "en": "🧭 Choose Vet by Direction",
        "uz": "🧭 Yo'nalish bo'yicha veterinar tanlash",
    },
    "choose_vet": {"ru": "👨‍⚕️ Выбрать ветеринара", "en": "👨‍⚕️ Choose veterinarian", "uz": "👨‍⚕️ Veterinarni tanlash"},
    "back": {"ru": "🔙 Назад", "en": "🔙 Back", "uz": "🔙 Orqaga"},
    "main_menu": {"ru": "🏠 Главное меню", "en": "🏠 Main Menu", "uz": "🏠 Asosiy menyu"},
    "dir_title": {
        "ru": "🧭 <b>Направления в ветеринарии</b>\n\nВыберите направление:",
        "en": "🧭 <b>Vet Directions</b>\n\nChoose direction:",
        "uz": "🧭 <b>Veterinariya yo'nalishlari</b>\n\nYo'nalishni tanlang:",
    },
    "dir_selected": {
        "ru": "🧭 <b>Направление:</b> {direction}",
        "en": "🧭 <b>Direction:</b> {direction}",
        "uz": "🧭 <b>Yo'nalish:</b> {direction}",
    },
    "no_vets": {
        "ru": "Пока нет доступных ветеринаров.",
        "en": "No available veterinarians yet.",
        "uz": "Hozircha mavjud veterinarlar yo'q.",
    },
    "no_vets_for_direction": {
        "ru": "По этому направлению пока нет доступных ветеринаров.",
        "en": "No available vets for this direction yet.",
        "uz": "Bu yo'nalish bo'yicha hozircha veterinar yo'q.",
    },
    "vet_default": {"ru": "Ветеринар", "en": "Veterinarian", "uz": "Veterinar"},
    "spec_default": {"ru": "Специалист", "en": "Specialist", "uz": "Mutaxassis"},
    "vets_title": {
        "ru": "👨‍⚕️ <b>Выберите ветеринара</b>",
        "en": "👨‍⚕️ <b>Choose veterinarian</b>",
        "uz": "👨‍⚕️ <b>Veterinarni tanlang</b>",
    },
    "contact_title": {
        "ru": "👨‍⚕️ <b>{name}</b>\n<b>Специализация:</b> {spec}\n<b>Телефон:</b> {phone}\n<b>Telegram:</b> {telegram}",
        "en": "👨‍⚕️ <b>{name}</b>\n<b>Specialization:</b> {spec}\n<b>Phone:</b> {phone}\n<b>Telegram:</b> {telegram}",
        "uz": "👨‍⚕️ <b>{name}</b>\n<b>Mutaxassislik:</b> {spec}\n<b>Telefon:</b> {phone}\n<b>Telegram:</b> {telegram}",
    },
    "open_chat": {"ru": "💬 Открыть чат", "en": "💬 Open chat", "uz": "💬 Chatni ochish"},
}


def _available_vets(exclude_user_id: int):
    return [(vet_id, profile) for vet_id, profile in vet_profiles.items() if vet_id != exclude_user_id]


def _lang(user_id: int) -> str:
    return user_languages.get(user_id, "ru")


def _direction_name(user_id: int, idx: int) -> str:
    language = _lang(user_id)
    item = DIRECTIONS[idx]
    return item.get(language, item["ru"])


def _direction_aliases(idx: int) -> list:
    item = DIRECTIONS[idx]
    return [value.lower() for value in item.values()]


def _vets_keyboard(user_id: int, vets, page: int, base_cb: str, back_cb: str) -> InlineKeyboardMarkup:
    start = page * VETS_PER_PAGE
    chunk = vets[start : start + VETS_PER_PAGE]
    rows = []

    for vet_id, vet in chunk:
        name = vet.get("vet_name") or tr(user_id, LOCAL["vet_default"])
        spec = vet.get("vet_specialization") or tr(user_id, LOCAL["spec_default"])
        rows.append([InlineKeyboardButton(text=f"👨‍⚕️ {name} ({spec})", callback_data=f"chat_with_{vet_id}")])

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="⬅️", callback_data=f"{base_cb}_{page - 1}"))
    if start + VETS_PER_PAGE < len(vets):
        nav.append(InlineKeyboardButton(text="➡️", callback_data=f"{base_cb}_{page + 1}"))
    if nav:
        rows.append(nav)

    rows.append([InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data=back_cb)])
    rows.append([InlineKeyboardButton(text=tr(user_id, LOCAL["main_menu"]), callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _directions_keyboard(user_id: int, page: int) -> InlineKeyboardMarkup:
    start = page * DIRECTIONS_PER_PAGE
    rows = []

    for idx in range(start, min(start + DIRECTIONS_PER_PAGE, len(DIRECTIONS))):
        rows.append([InlineKeyboardButton(text=_direction_name(user_id, idx), callback_data=f"vet_dir_{idx}")])

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="⬅️", callback_data=f"menu_vet_directions_{page - 1}"))
    if start + DIRECTIONS_PER_PAGE < len(DIRECTIONS):
        nav.append(InlineKeyboardButton(text="➡️", callback_data=f"menu_vet_directions_{page + 1}"))
    if nav:
        rows.append(nav)

    rows.append([InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="menu_vet_chat")])
    rows.append([InlineKeyboardButton(text=tr(user_id, LOCAL["main_menu"]), callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


@dp.callback_query(F.data == "menu_vet_chat")
async def vet_chat_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    await safe_edit_message(
        callback.message,
        tr(user_id, LOCAL["title"]),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["directions"]), callback_data="menu_vet_directions_0")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["choose_vet"]), callback_data="menu_vet_choose_all_0")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="back_to_menu")],
            ]
        ),
        parse_mode=ParseMode.HTML,
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("menu_vet_directions_"))
async def vet_directions_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    try:
        page = int(callback.data.replace("menu_vet_directions_", ""))
    except ValueError:
        page = 0

    await safe_edit_message(
        callback.message,
        tr(user_id, LOCAL["dir_title"]),
        reply_markup=_directions_keyboard(user_id, page),
        parse_mode=ParseMode.HTML,
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("vet_dir_"))
async def vet_direction_selected(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    try:
        idx = int(callback.data.replace("vet_dir_", ""))
        direction = _direction_name(user_id, idx)
    except (ValueError, IndexError):
        await callback.answer()
        return

    text = tr(user_id, LOCAL["dir_selected"]).format(direction=direction)
    vets = _available_vets(user_id)
    aliases = _direction_aliases(idx)
    matched = [item for item in vets if any(alias in (item[1].get("vet_specialization", "").lower()) for alias in aliases)]

    if not matched:
        text += f"\n\n{tr(user_id, LOCAL['no_vets_for_direction'])}"

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=tr(user_id, LOCAL["choose_vet"]), callback_data=f"menu_vet_choose_dir_{idx}_0")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["main_menu"]), callback_data="back_to_menu")],
                [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="menu_vet_chat")],
            ]
        ),
        parse_mode=ParseMode.HTML,
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("menu_vet_choose_all_"))
async def choose_vet_all(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    try:
        page = int(callback.data.replace("menu_vet_choose_all_", ""))
    except ValueError:
        page = 0

    vets = _available_vets(user_id)
    if not vets:
        await safe_edit_message(
            callback.message,
            tr(user_id, LOCAL["no_vets"]),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="menu_vet_chat")],
                    [InlineKeyboardButton(text=tr(user_id, LOCAL["main_menu"]), callback_data="back_to_menu")],
                ]
            ),
        )
        await callback.answer()
        return

    await safe_edit_message(
        callback.message,
        tr(user_id, LOCAL["vets_title"]),
        reply_markup=_vets_keyboard(user_id, vets, page, "menu_vet_choose_all", "menu_vet_chat"),
        parse_mode=ParseMode.HTML,
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("menu_vet_choose_dir_"))
async def choose_vet_by_direction(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    payload = callback.data.replace("menu_vet_choose_dir_", "")
    try:
        idx_raw, page_raw = payload.rsplit("_", 1)
        idx = int(idx_raw)
        page = int(page_raw)
        aliases = _direction_aliases(idx)
    except (ValueError, IndexError):
        await callback.answer()
        return

    vets = _available_vets(user_id)
    filtered = [item for item in vets if any(alias in (item[1].get("vet_specialization", "").lower()) for alias in aliases)]
    if not filtered:
        await safe_edit_message(
            callback.message,
            tr(user_id, LOCAL["no_vets_for_direction"]),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data=f"vet_dir_{idx}")],
                    [InlineKeyboardButton(text=tr(user_id, LOCAL["main_menu"]), callback_data="back_to_menu")],
                ]
            ),
        )
        await callback.answer()
        return

    await safe_edit_message(
        callback.message,
        tr(user_id, LOCAL["vets_title"]),
        reply_markup=_vets_keyboard(
            user_id,
            filtered,
            page,
            f"menu_vet_choose_dir_{idx}",
            f"vet_dir_{idx}",
        ),
        parse_mode=ParseMode.HTML,
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("chat_with_"))
async def chat_with_vet(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    try:
        vet_id = int(callback.data.replace("chat_with_", ""))
    except ValueError:
        await callback.answer()
        return

    vet = vet_profiles.get(vet_id)
    if not vet:
        await callback.answer(tr(user_id, LOCAL["no_vets"]), show_alert=False)
        return

    name = vet.get("vet_name") or tr(user_id, LOCAL["vet_default"])
    spec = vet.get("vet_specialization") or tr(user_id, LOCAL["spec_default"])
    phone = vet.get("vet_phone") or "-"
    tg = vet.get("vet_telegram") or "-"

    message_text = tr(user_id, LOCAL["contact_title"]).format(name=name, spec=spec, phone=phone, telegram=tg)
    buttons = []
    username = (tg or "").strip().lstrip("@")
    if username and username != "-":
        buttons.append([InlineKeyboardButton(text=tr(user_id, LOCAL["open_chat"]), url=f"https://t.me/{username}")])
    buttons.append([InlineKeyboardButton(text=tr(user_id, LOCAL["back"]), callback_data="menu_vet_chat")])

    await safe_edit_message(
        callback.message,
        message_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode=ParseMode.HTML,
    )
    await callback.answer()

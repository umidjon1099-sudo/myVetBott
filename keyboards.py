from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_data import TEXTS, UZBEK_CITIES

_get_text = None


def configure_text_provider(get_text):
    global _get_text
    _get_text = get_text


def _text(user_id, key):
    if _get_text:
        return _get_text(user_id, key)
    text_dict = TEXTS.get(key, {})
    return text_dict.get("ru", key)


def create_reminder_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏰ Один раз", callback_data="reminder_one_time")],
        [InlineKeyboardButton(text="🔄 Ежедневно", callback_data="reminder_daily")],
        [InlineKeyboardButton(text="📆 Еженедельно", callback_data="reminder_weekly")],
        [InlineKeyboardButton(text="⚙️ Настроить дни", callback_data="reminder_custom")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_reminders")],
    ])


def create_cities_keyboard():
    buttons = []
    row = []

    for city_key in UZBEK_CITIES:
        city_name = TEXTS.get(city_key, {}).get("ru", city_key)
        row.append(InlineKeyboardButton(text=city_name, callback_data=f"city_{city_key}"))

        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append([InlineKeyboardButton(text="📍 Найти по геолокации", callback_data="find_by_location")])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_animal_type_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐕 Собака", callback_data="animal_dog")],
        [InlineKeyboardButton(text="🐱 Кошка", callback_data="animal_cat")],
        [InlineKeyboardButton(text="🐹 Грызуны", callback_data="animal_rodent")],
        [InlineKeyboardButton(text="🐦 Птицы", callback_data="animal_bird")],
        [InlineKeyboardButton(text="🐠 Рыбки", callback_data="animal_fish")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")],
    ])


def create_feeding_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Домашние животные", callback_data="feeding_domestic")],
        [InlineKeyboardButton(text="🐄 Сельскохозяйственные", callback_data="feeding_farm")],
        [InlineKeyboardButton(text="🦎 Экзотические", callback_data="feeding_exotic")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")],
    ])


def create_domestic_animals_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐕 Собаки", callback_data="feed_dog")],
        [InlineKeyboardButton(text="🐱 Кошки", callback_data="feed_cat")],
        [InlineKeyboardButton(text="🐹 Грызуны", callback_data="feed_rodent")],
        [InlineKeyboardButton(text="🐦 Птицы", callback_data="feed_bird")],
        [InlineKeyboardButton(text="🐠 Рыбки", callback_data="feed_fish")],
        [InlineKeyboardButton(text="🐢 Рептилии", callback_data="feed_reptile")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_feeding")],
    ])


def create_language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")],
    ])


def get_main_menu(user_id: int = None):
    menu_buttons = [
        [InlineKeyboardButton(text=_text(user_id, "profile_big"), callback_data="menu_profile")],
        [
            InlineKeyboardButton(text=_text(user_id, "ads"), callback_data="menu_ads"),
            InlineKeyboardButton(text=_text(user_id, "news"), callback_data="menu_news"),
        ],
        [
            InlineKeyboardButton(text=_text(user_id, "pet_shop"), callback_data="menu_pet_shop"),
            InlineKeyboardButton(text=_text(user_id, "pet_facts"), callback_data="menu_facts"),
        ],
        [
            InlineKeyboardButton(text=_text(user_id, "feeding_guide"), callback_data="menu_feeding"),
            InlineKeyboardButton(text=_text(user_id, "symptoms"), callback_data="menu_symptoms"),
        ],
        [
            InlineKeyboardButton(text=_text(user_id, "clinics"), callback_data="menu_clinics"),
            InlineKeyboardButton(text=_text(user_id, "pharmacies"), callback_data="menu_pharmacies"),
        ],
        [
            InlineKeyboardButton(text=_text(user_id, "reminders"), callback_data="menu_reminders"),
            InlineKeyboardButton(text=_text(user_id, "shelters"), callback_data="menu_shelters"),
        ],
        [
            InlineKeyboardButton(text=_text(user_id, "vet_chat"), callback_data="menu_vet_chat"),
            InlineKeyboardButton(text=_text(user_id, "appointment"), callback_data="menu_appointment"),
        ],
        [
            InlineKeyboardButton(text=_text(user_id, "history"), callback_data="menu_history"),
            InlineKeyboardButton(text=_text(user_id, "language"), callback_data="menu_language"),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=menu_buttons)


def get_back_to_menu_button(user_id: int = None):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
    ])


def get_profile_menu(user_id: int = None):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_text(user_id, "create_profile"), callback_data="create_profile")],
        [InlineKeyboardButton(text=_text(user_id, "create_vet_profile"), callback_data="create_vet_profile")],
        [InlineKeyboardButton(text=_text(user_id, "view_profile"), callback_data="profile_view")],
        [InlineKeyboardButton(text=_text(user_id, "view_vet_profile"), callback_data="vet_profile_view")],
        [InlineKeyboardButton(text=_text(user_id, "edit_profile"), callback_data="edit_profile")],
        [InlineKeyboardButton(text=_text(user_id, "clear_profile"), callback_data="profile_clear")],
        [InlineKeyboardButton(text=_text(user_id, "back_to_menu"), callback_data="back_to_menu")],
    ])


def get_ads_menu(user_id: int = None):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_text(user_id, "post_ad"), callback_data="post_ad")],
        [InlineKeyboardButton(text=_text(user_id, "view_ads"), callback_data="view_ads")],
        [InlineKeyboardButton(text=_text(user_id, "my_ads"), callback_data="my_ads")],
        [InlineKeyboardButton(text=_text(user_id, "back_to_menu"), callback_data="back_to_menu")],
    ])


def get_reminders_menu(user_id: int = None):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_text(user_id, "add_reminder"), callback_data="reminder_add")],
        [InlineKeyboardButton(text=_text(user_id, "my_reminders"), callback_data="reminder_list")],
        [InlineKeyboardButton(text=_text(user_id, "back_to_menu"), callback_data="back_to_menu")],
    ])

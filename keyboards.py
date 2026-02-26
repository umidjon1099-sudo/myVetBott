from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_data import TEXTS, UZBEK_CITIES
from data_store import user_languages

_get_text = None


def configure_text_provider(get_text):
    global _get_text
    _get_text = get_text


def _text(user_id, key):
    if _get_text:
        return _get_text(user_id, key)
    text_dict = TEXTS.get(key, {})
    return text_dict.get("ru", key)

_KBD_TEXTS = {
    "cancel": {"ru": "❌ Отмена", "en": "❌ Cancel", "uz": "❌ Bekor qilish"},
    "back": {"ru": "🔙 Назад", "en": "🔙 Back", "uz": "🔙 Orqaga"},
    "find_on_map": {"ru": "📍 Показать на карте", "en": "📍 Show on map", "uz": "📍 Xaritada ko'rsatish"},
    "animal_dog": {"ru": "🐕 Собаки", "en": "🐕 Dogs", "uz": "🐕 Itlar"},
    "animal_cat": {"ru": "🐱 Кошки", "en": "🐱 Cats", "uz": "🐱 Mushuklar"},
    "animal_cow": {"ru": "🐄 Коровы", "en": "🐄 Cows", "uz": "🐄 Sigirlar"},
    "animal_sheep": {"ru": "🐏 Бараны / Овцы", "en": "🐏 Rams / Sheep", "uz": "🐏 Qo'y / Qo'chqor"},
    "animal_rodent": {"ru": "🐹 Грызуны", "en": "🐹 Rodents", "uz": "🐹 Kemiruvchilar"},
    "animal_bird": {"ru": "🐦 Птицы", "en": "🐦 Birds", "uz": "🐦 Qushlar"},
    "animal_fish": {"ru": "🐠 Рыбки", "en": "🐠 Fish", "uz": "🐠 Baliqlar"},
    "animal_exotic": {"ru": "🦎 Экзотические", "en": "🦎 Exotic", "uz": "🦎 Ekzotik"},
    "feed_dog": {"ru": "🐕 Собаки", "en": "🐕 Dogs", "uz": "🐕 Itlar"},
    "feed_cat": {"ru": "🐱 Кошки", "en": "🐱 Cats", "uz": "🐱 Mushuklar"},
    "feed_rodent": {"ru": "🐹 Грызуны", "en": "🐹 Rodents", "uz": "🐹 Kemiruvchilar"},
    "feed_bird": {"ru": "🐦 Птицы", "en": "🐦 Birds", "uz": "🐦 Qushlar"},
    "feed_fish": {"ru": "🐠 Рыбки", "en": "🐠 Fish", "uz": "🐠 Baliqlar"},
    "feed_reptile": {"ru": "🐢 Рептилии", "en": "🐢 Reptiles", "uz": "🐢 Sudralib yuruvchilar"},
}


def _lang(user_id):
    return user_languages.get(user_id, "ru")


def _kbd_text(user_id, key):
    lang = _lang(user_id)
    item = _KBD_TEXTS.get(key, {})
    return item.get(lang, item.get("ru", key))


def create_reminder_keyboard(user_id: int = None):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_text(user_id, "one_time"), callback_data="reminder_one_time")],
        [InlineKeyboardButton(text=_text(user_id, "daily"), callback_data="reminder_daily")],
        [InlineKeyboardButton(text=_text(user_id, "weekly"), callback_data="reminder_weekly")],
        [InlineKeyboardButton(text=_text(user_id, "custom"), callback_data="reminder_custom")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "back"), callback_data="menu_reminders")],
    ])


def create_cities_keyboard(user_id: int = None):
    buttons = []
    row = []

    for city_key in UZBEK_CITIES:
        city_name = _text(user_id, city_key)
        row.append(InlineKeyboardButton(text=city_name, callback_data=f"city_{city_key}"))

        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append([InlineKeyboardButton(text=_text(user_id, "find_by_location"), callback_data="find_by_location")])
    buttons.append([InlineKeyboardButton(text=_kbd_text(user_id, "back"), callback_data="back_to_menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_animal_type_keyboard(user_id: int = None):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_kbd_text(user_id, "animal_dog"), callback_data="animal_dog")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "animal_cat"), callback_data="animal_cat")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "animal_cow"), callback_data="animal_cow")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "animal_sheep"), callback_data="animal_sheep")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "animal_rodent"), callback_data="animal_rodent")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "animal_bird"), callback_data="animal_bird")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "animal_fish"), callback_data="animal_fish")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "animal_exotic"), callback_data="animal_exotic")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "back"), callback_data="back_to_menu")],
    ])


def create_feeding_keyboard(user_id: int = None):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🏠 {_text(user_id, 'domestic_pets')}", callback_data="feeding_domestic")],
        [InlineKeyboardButton(text=f"🐄 {_text(user_id, 'farm_animals')}", callback_data="feeding_farm")],
        [InlineKeyboardButton(text=f"🦎 {_text(user_id, 'exotic_animals')}", callback_data="feeding_exotic")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "back"), callback_data="back_to_menu")],
    ])


def create_domestic_animals_keyboard(user_id: int = None):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_kbd_text(user_id, "feed_dog"), callback_data="feed_dog")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "feed_cat"), callback_data="feed_cat")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "feed_rodent"), callback_data="feed_rodent")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "feed_bird"), callback_data="feed_bird")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "feed_fish"), callback_data="feed_fish")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "feed_reptile"), callback_data="feed_reptile")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "back"), callback_data="menu_feeding")],
    ])


def create_language_keyboard(user_id: int = None):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz")],
        [InlineKeyboardButton(text=_kbd_text(user_id, "back"), callback_data="back_to_menu")],
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

from os import mkdir, makedirs

import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import json


# --- КОНФИГУРАЦИЯddd ---
API_TOKEN = "8467556633:AAFwl2sXSzq-3SCSHfp0TCSr4vbduIHOOlU"  # myvet glavniyy
#API_TOKEN = "8489986940:AAHwTZeAUYXFYmi8x6ZBoVIJwtF-jJ3TNqs"  # Vet_Hel_per_Bot

# Настраиваем логгирование
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Хранилище состояний и данных
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=storage)

# --- ХРАНЕНИЕ ДАННЫХ (в памяти) ---
user_profiles = {}  # {user_id: {данные профиля}}
vet_profiles = {}  # {user_id: {данные ветеринара}}
user_symptoms = {}  # {user_id: [симптомы]}
user_reminders = {}  # {user_id: [напоминания]}
user_history = {}  # {user_id: [история]}
user_languages = {}  # {user_id: "ru"/"en"/"uz"}
user_ads = {}  # {user_id: [объявления]}
news = []  # Новости
pet_facts = []  # Интересные факты
feeding_guides = {}  # Информация о кормлении
appointments = {}  # Записи на прием {user_id: []}
messages_to_delete = {}  # Для управления сообщениями


makedirs ('Главные кнопки меню', exist_ok=True)

# ========== ВСЕ ТЕКСТЫ БОТА НА 3 ЯЗЫКАХ ==========
TEXTS = {
    # Главные кнопки меню
    "profile_big": {
        "ru": "👤 МОЙ ПРОФИЛЬ",
        "en": "👤 MY PROFILE",
        "uz": "👤 MENING PROFILIM"
    },
    "ads": {
        "ru": "📢 Объявления",
        "en": "📢 Ads",
        "uz": "📢 E'lonlar"
    },
    "news": {
        "ru": "📰 Новости",
        "en": "📰 News",
        "uz": "📰 Yangiliklar"
    },
    "pet_shop": {
        "ru": "🛍️ Зоомагазин",
        "en": "🛍️ Pet Shop",
        "uz": "🛍️ Hayvonlar do'koni"
    },
    "pet_facts": {
        "ru": "🤔 Интересные факты",
        "en": "🤔 Interesting Facts",
        "uz": "🤔 Qiziqarli faktlar"
    },
    "feeding_guide": {
        "ru": "🍖 Кормление питомца",
        "en": "🍖 Feeding Guide",
        "uz": "🍖 Hayvonni oziqlantirish"
    },
    "symptoms": {
        "ru": "🩺 Проверка симптомов",
        "en": "🩺 Check Symptoms",
        "uz": "🩺 Simptomlarni tekshirish"
    },
    "clinics": {
        "ru": "📍 Клиники",
        "en": "📍 Clinics",
        "uz": "📍 Klinikalar"
    },
    "pharmacies": {
        "ru": "💊 Аптеки",
        "en": "💊 Pharmacies",
        "uz": "💊 Dorixonlar"
    },
    "reminders": {
        "ru": "⏰ Напоминания",
        "en": "⏰ Reminders",
        "uz": "⏰ Eslatmalar"
    },
    "shelters": {
        "ru": "🏠 Приюты",
        "en": "🏠 Shelters",
        "uz": "🏠 Boshpana uylari"
    },
    "vet_chat": {
        "ru": "💬 Чат с ветер.",
        "en": "💬 Vet Chat",
        "uz": "💬 Veterinar chat"
    },
    "history": {
        "ru": "📋 История",
        "en": "📋 History",
        "uz": "📋 Tarix"
    },
    "language": {
        "ru": "🌍 Языкaaaaa",
        "en": "🌍 Languageaaaa",
        "uz": "🌍 Tilaaaa"
    },
    "mini_app": {
        "ru": "📱 Mini App",
        "en": "📱 Mini App",
        "uz": "📱 Mini App"
    },
    "appointment": {
        "ru": "📅 Запись к врачу",
        "uz": "📅 Shifokorga yozilish"
    },

    # Общие тексты
    "welcome": {
        "ru": "Привет, {name}! 🐾\nЯ PetHelperBot - твой цифровой помощник для заботы о питомце.\nВыбери опцию ниже:",
        "en": "Hello, {name}! 🐾\nI'm PetHelperBot - your digital pet care assistant.\nChoose an option below:",
        "uz": "Salom, {name}! 🐾\nMen PetHelperBotman - hayvoningizga g'amxo'rlik qilishda raqamli yordamchingiz.\nQuyidagi variantni tanlang:"
    },
    "main_menu": {
        "ru": "Главное меню:",
        "en": "Main menu:",
        "uz": "Asosiy menyu:"
    },
    "back_to_menu": {
        "ru": "🔙 Главное меню",
        "en": "🔙 Main Menu",
        "uz": "🔙 Asosiy menyu"
    },

    # Профиль
    "profile_section": {
        "ru": "👤 <b>Мой профиль</b>\n\nВыберите тип профиля для создания:",
        "en": "👤 <b>My Profile</b>\n\nChoose profile type to create:",
        "uz": "👤 <b>Mening profilingiz</b>\n\nYaratish uchun profil turini tanlang:"
    },
    "create_profile": {
        "ru": "✏️ Создать профиль",
        "en": "✏️ Create Profile",
        "uz": "✏️ Profil yaratish"
    },
    "create_vet_profile": {
        "ru": "👨‍⚕️ Создать профиль ветеринара",
        "en": "👨‍⚕️ Create Vet Profile",
        "uz": "👨‍⚕️ Veterinar profilini yaratish"
    },
    "view_profile": {
        "ru": "👁️ Просмотреть профиль",
        "en": "👁️ View Profile",
        "uz": "👁️ Profilni ko'rish"
    },
    "view_vet_profile": {
        "ru": "👨‍⚕️ Просмотреть профиль ветеринара",
        "en": "👨‍⚕️ View Vet Profile",
        "uz": "👨‍⚕️ Veterinar profilini ko'rish"
    },
    "edit_profile": {
        "ru": "🔄 Изменить профиль",
        "en": "🔄 Edit Profile",
        "uz": "🔄 Profilni o'zgartirish"
    },
    "clear_profile": {
        "ru": "🗑️ Очистить профиль",
        "en": "🗑️ Clear Profile",
        "uz": "🗑️ Profilni tozalash"
    },
    "profile_empty": {
        "ru": "❌ Профиль не заполнен!\n\nНажмите 'Создать профиль'",
        "en": "❌ Profile is empty!\n\nClick 'Create Profile'",
        "uz": "❌ Profil to'ldirilmagan!\n\n'Profil yaratish' tugmasini bosing"
    },
    "vet_profile_empty": {
        "ru": "❌ Профиль ветеринара не заполнен!\n\nНажмите 'Создать профиль ветеринара'",
        "en": "❌ Vet profile is empty!\n\nClick 'Create Vet Profile'",
        "uz": "❌ Veterinar profili to'ldirilmagan!\n\n'Veterinar profilini yaratish' tugmasini bosing"
    },

    # Тексты для создания профиля
    "enter_owner_name": {
        "ru": "Введите ваше имя:",
        "en": "Enter your name:",
        "uz": "Ismingizni kiriting:"
    },
    "enter_owner_phone": {
        "ru": "Введите ваш номер телефона:",
        "en": "Enter your phone number:",
        "uz": "Telefon raqamingizni kiriting:"
    },
    "enter_city": {
        "ru": "Введите ваш город:",
        "en": "Enter your city:",
        "uz": "Shahringizni kiriting:"
    },
    "enter_pet_name": {
        "ru": "Введите имя питомца:",
        "en": "Enter pet's name:",
        "uz": "Hayvoningizning ismini kiriting:"
    },
    "enter_pet_type": {
        "ru": "Введите вид питомца (собака, кошка и т.д.):",
        "en": "Enter pet type (dog, cat, etc.):",
        "uz": "Hayvon turini kiriting (it, mushuk va h.k.):"
    },

    # Для владельцев животных
    "owner_profile": {
        "ru": "👤 ПРОФИЛЬ ВЛАДЕЛЬЦА",
        "en": "👤 OWNER PROFILE",
        "uz": "👤 EGASI PROFILI"
    },
    "vet_profile": {
        "ru": "👨‍⚕️ ПРОФИЛЬ ВЕТЕРИНАРА",
        "en": "👨‍⚕️ VET PROFILE",
        "uz": "👨‍⚕️ VETERINAR PROFILI"
    },

    # Клиники и аптеки
    "clinics_section": {
        "ru": "📍 <b>Ветеринарные клиники</b>\n\nВыберите город для поиска:",
        "en": "📍 <b>Veterinary Clinics</b>\n\nChoose city to search:",
        "uz": "📍 <b>Veterinariya klinikalari</b>\n\nQidirish uchun shaharni tanlang:"
    },
    "pharmacies_section": {
        "ru": "💊 <b>Ветеринарные аптеки</b>\n\nВыберите город для поиска:",
        "en": "💊 <b>Veterinary Pharmacies</b>\n\nChoose city to search:",
        "uz": "💊 <b>Veterinariya dorixonlari</b>\n\nQidirish uchun shaharni tanlang:"
    },
    "find_by_location": {
        "ru": "📍 Найти по геолокации",
        "en": "📍 Find by location",
        "uz": "📍 Joylashuv bo'yicha topish"
    },

    # Города Узбекистана
    "tashkent": {"ru": "Ташкент", "en": "Tashkent", "uz": "Toshkent"},
    "samarkand": {"ru": "Самарканд", "en": "Samarkand", "uz": "Samarqand"},
    "bukhara": {"ru": "Бухара", "en": "Bukhara", "uz": "Buxoro"},
    "khiva": {"ru": "Хива", "en": "Khiva", "uz": "Xiva"},
    "andijan": {"ru": "Андижан", "en": "Andijan", "uz": "Andijon"},
    "namangan": {"ru": "Наманган", "en": "Namangan", "uz": "Namangan"},
    "fergana": {"ru": "Фергана", "en": "Fergana", "uz": "Farg'ona"},
    "nukus": {"ru": "Нукус", "en": "Nukus", "uz": "Nukus"},
    "urgench": {"ru": "Ургенч", "en": "Urgench", "uz": "Urganch"},
    "karshi": {"ru": "Карши", "en": "Karshi", "uz": "Qarshi"},
    "jizzakh": {"ru": "Джизак", "en": "Jizzakh", "uz": "Jizzax"},
    "navoi": {"ru": "Навои", "en": "Navoi", "uz": "Navoiy"},
    "termez": {"ru": "Термез", "en": "Termez", "uz": "Termiz"},

    # Напоминания
    "reminders_section": {
        "ru": "⏰ <b>Управление напоминаниями</b>\n\nСоздавайте напоминания о лекарствах, вакцинациях и процедурах:",
        "en": "⏰ <b>Manage Reminders</b>\n\nCreate reminders for medications, vaccinations and procedures:",
        "uz": "⏰ <b>Eslatmalarni boshqarish</b>\n\nDori-darmonlar, emlashlar va protseduralar uchun eslatmalar yarating:"
    },
    "add_reminder": {
        "ru": "➕ Добавить напоминание",
        "en": "➕ Add reminder",
        "uz": "➕ Eslatma qo'shish"
    },
    "my_reminders": {
        "ru": "📋 Мои напоминания",
        "en": "📋 My reminders",
        "uz": "📋 Mening eslatmalarim"
    },
    "reminder_types": {
        "ru": "⏰ <b>Тип напоминания:</b>\n\nВыберите тип:",
        "en": "⏰ <b>Reminder Type:</b>\n\nChoose type:",
        "uz": "⏰ <b>Eslatma turi:</b>\n\nTurini tanlang:"
    },
    "one_time": {
        "ru": "⏰ Один раз",
        "en": "⏰ One time",
        "uz": "⏰ Bir marta"
    },
    "daily": {
        "ru": "🔄 Ежедневно",
        "en": "🔄 Daily",
        "uz": "🔄 Har kuni"
    },
    "weekly": {
        "ru": "📆 Еженедельно",
        "en": "📆 Weekly",
        "uz": "📆 Har hafta"
    },
    "custom": {
        "ru": "⚙️ Настроить",
        "en": "⚙️ Custom",
        "uz": "⚙️ Moslashtirish"
    },

    # Приюты
    "shelters_section": {
        "ru": "🏠 <b>Приюты для животных</b>\n\nВыберите город для поиска приютов:",
        "en": "🏠 <b>Animal Shelters</b>\n\nChoose city to search shelters:",
        "uz": "🏠 <b>Hayvonlar boshpana uylari</b>\n\nBoshpana uylarini qidirish uchun shaharni tanlang:"
    },

    # Объявления
    "ads_section": {
        "ru": "📢 <b>Объявления</b>\n\nПодайте объявление или посмотрите существующие:",
        "en": "📢 <b>Advertisements</b>\n\nPost an ad or view existing ones:",
        "uz": "📢 <b>E'lonlar</b>\n\nE'lon joylashtiring yoki mavjud e'lonlarni ko'ring:"
    },
    "post_ad": {
        "ru": "📝 Подать объявление",
        "en": "📝 Post ad",
        "uz": "📝 E'lon joylashtirish"
    },
    "view_ads": {
        "ru": "👁️ Смотреть объявления",
        "en": "👁️ View ads",
        "uz": "👁️ E'lonlarni ko'rish"
    },
    "my_ads": {
        "ru": "📋 Мои объявления",
        "en": "📋 My ads",
        "uz": "📋 Mening e'lonlarim"
    },

    # Новости
    "news_section": {
        "ru": "📰 <b>Новости о животных</b>\n\nПоследние новости из мира животных:",
        "en": "📰 <b>Pet News</b>\n\nLatest news from the animal world:",
        "uz": "📰 <b>Hayvonlar yangiliklari</b>\n\nHayvonlar olamidan so'nggi yangiliklar:"
    },
    "latest_news": {
        "ru": "🆕 Последние новости",
        "en": "🆕 Latest news",
        "uz": "🆕 So'nggi yangiliklar"
    },

    # Зоомагазин
    "pet_shop_section": {
        "ru": "🛍️ <b>Зоомагазины</b>\n\nНайдите зоомагазины в вашем городе:",
        "en": "🛍️ <b>Pet Shops</b>\n\nFind pet shops in your city:",
        "uz": "🛍️ <b>Hayvonlar do'konlari</b>\n\nShaharingizdagi hayvonlar do'konlarini toping:"
    },

    # Интересные факты
    "facts_section": {
        "ru": "🤔 <b>Интересные факты о животных</b>\n\nУзнайте интересные факты:",
        "en": "🤔 <b>Interesting Animal Facts</b>\n\nLearn interesting facts:",
        "uz": "🤔 <b>Hayvonlar haqida qiziqarli faktlar</b>\n\nQiziqarli faktlarni bilib oling:"
    },
    "random_fact": {
        "ru": "🎲 Случайный факт",
        "en": "🎲 Random fact",
        "uz": "🎲 Tasodifiy fakt"
    },

    # Кормление
    "feeding_section": {
        "ru": "🍖 <b>Правильное кормление питомца</b>\n\nВыберите тип животного:",
        "en": "🍖 <b>Proper Pet Feeding</b>\n\nChoose animal type:",
        "uz": "🍖 <b>Hayvonni to'g'ri oziqlantirish</b>\n\nHayvon turini tanlang:"
    },
    "domestic_pets": {
        "ru": "🏠 Домашние животные",
        "en": "🏠 Domestic Pets",
        "uz": "🏠 Uy hayvonlari"
    },
    "farm_animals": {
        "ru": "🐄 Сельскохозяйственные",
        "en": "🐄 Farm Animals",
        "uz": "🐄 Ferma hayvonlari"
    },
    "exotic_animals": {
        "ru": "🦎 Экзотические",
        "en": "🦎 Exotic Animals",
        "uz": "🦎 Ekzotik hayvonlar"
    },

    # Язык
    "choose_language": {
        "ru": "🌍 <b>Выберите язык:</b>",
        "en": "🌍 <b>Choose language:</b>",
        "uz": "🌍 <b>Tilni tanlang:</b>"
    },

    # Запись на прием
    "appointment_section": {
        "ru": "📅 <b>Запись к ветеринару</b>\n\nВыберите ветеринара для записи:",
        "en": "📅 <b>Vet Appointment</b>\n\nChoose veterinarian for appointment:",
        "uz": "📅 <b>Veterinarga yozilish</b>\n\nYozilish uchun veterinarni tanlang:"
    },

    # Чат с ветеринаром
    "vet_chat_section": {
        "ru": "💬 <b>Чат с ветеринаром</b>\n\nВыберите ветеринара для консультации:",
        "en": "💬 <b>Vet Chat</b>\n\nChoose veterinarian for consultation:",
        "uz": "💬 <b>Veterinar bilan chat</b>\n\nMaslahat olish uchun veterinarni tanlang:"
    }
}

# Города Узбекистана
UZBEK_CITIES = [
    "tashkent", "samarkand", "bukhara", "khiva", "andijan",
    "namangan", "fergana", "nukus", "urgench", "karshi",
    "jizzakh", "navoi", "termez"
]

# Данные о клиниках, аптеках и приютах (примерные данные)
CLINICS_DATA = {
    "tashkent": [
        "🏥 <b>Vet Clinic 'Pet Care'</b>\n📍 Mirzo Ulug'bek tumani\n📞 +998 71 123 45 67\n🕒 24/7",
        "🏥 <b>Animal Hospital Tashkent</b>\n📍 Yunusobod tumani\n📞 +998 71 234 56 78\n🕒 08:00-22:00",
        "🏥 <b>Doctor Vet Center</b>\n📍 Shayxontohur tumani\n📞 +998 71 345 67 89\n🕒 09:00-20:00"
    ],
    "samarkand": [
        "🏥 <b>Samarkand Vet Clinic</b>\n📍 Registon ko'chasi\n📞 +998 66 123 45 67\n🕒 09:00-19:00",
        "🏥 <b>Animal Care Samarqand</b>\n📍 Amir Temur ko'chasi\n📞 +998 66 234 56 78\n🕒 08:00-21:00"
    ]
}

PHARMACIES_DATA = {
    "tashkent": [
        "💊 <b>Vet Pharmacy #1</b>\n📍 Chilonzor tumani\n📞 +998 71 111 22 33\n🕒 08:00-23:00",
        "💊 <b>Animal Drugs Center</b>\n📍 Yakkasaroy tumani\n📞 +998 71 222 33 44\n🕒 24/7",
        "💊 <b>Pet Med Tashkent</b>\n📍 Mirabad tumani\n📞 +998 71 333 44 55\n🕒 09:00-22:00"
    ]
}

SHELTERS_DATA = {
    "tashkent": [
        "🏠 <b>Tashkent Animal Shelter</b>\n📍 Qibray tumani\n📞 +998 71 444 55 66\n🐕 50+ animals",
        "🏠 <b>Hope for Pets Shelter</b>\n📍 Olmazor tumani\n📞 +998 71 555 66 77\n🐱 30+ animals"
    ]
}

# Интересные факты о животных
ANIMAL_FACTS = [
    "🐕 Собаки понимают до 250 слов и жестов, считают до пяти и могут решать простейшие математические задачи.",
    "🐱 Кошки спят около 70% своей жизни.",
    "🐰 Кролики могут видеть позади себя, не поворачивая головы.",
    "🐦 Попугаи могут жить более 80 лет.",
    "🐠 Золотые рыбки имеют память около 3 месяцев.",
    "🦜 Некоторые виды попугаев могут имитировать человеческую речь почти идеально.",
    "🐹 Хомяки могут пробежать до 8 км за ночь в своем колесе.",
    "🐢 Черепахи могут жить более 100 лет.",
    "🦎 Некоторые ящерицы могут отбрасывать хвост при опасности.",
    "🐭 Мыши могут смеяться, когда их щекочут."
]

# Информация о кормлении животных
FEEDING_INFO = {
    "dog": {
        "ru": "🐕 <b>Кормление собак:</b>\n\n• Кормите 2-3 раза в день\n• Соблюдайте режим кормления\n• Сухой корм должен быть высокого качества\n• Всегда обеспечьте доступ к свежей воде\n• Избегайте: шоколад, лук, виноград, орехи макадамия",
        "en": "🐕 <b>Feeding Dogs:</b>\n\n• Feed 2-3 times a day\n• Maintain feeding schedule\n• Dry food should be high quality\n• Always provide fresh water\n• Avoid: chocolate, onions, grapes, macadamia nuts",
        "uz": "🐕 <b>Itlarni oziqlantirish:</b>\n\n• Kuniga 2-3 marta ozuqa bering\n• Oziqlantirish jadvaliga rioya qiling\n• Quruq ozuqa yuqori sifatli bo'lishi kerak\n• Har doim toza suv ta'minlang\n• Qochish: shokolad, piyoz, uzum, makadamiya yong'oqlari"
    },
    "cat": {
        "ru": "🐱 <b>Кормление кошек:</b>\n\n• Кормите маленькими порциями 3-4 раза в день\n• Кошки - плотоядные, им нужно мясо\n• Обеспечьте доступ к свежей воде\n• Избегайте: молоко (у взрослых кошек), лук, шоколад",
        "en": "🐱 <b>Feeding Cats:</b>\n\n• Feed small portions 3-4 times a day\n• Cats are carnivores, they need meat\n• Provide access to fresh water\n• Avoid: milk (in adult cats), onions, chocolate",
        "uz": "🐱 <b>Mushuklarni oziqlantirish:</b>\n\n• Kuniga 3-4 marta kichik porsiyalarda ozuqa bering\n• Mushuklar yirtqich hayvonlar, ularga go'sht kerak\n• Toza suvga kirish imkoniyatini ta'minlang\n• Qochish: sut (katta mushuklarda), piyoz, shokolad"
    },
    "bird": {
        "ru": "🐦 <b>Кормление птиц:</b>\n\n• Специальные зерновые смеси\n• Свежие фрукты и овощи\n• Кальциевые добавки\n• Чистая вода ежедневно",
        "en": "🐦 <b>Feeding Birds:</b>\n\n• Special grain mixtures\n• Fresh fruits and vegetables\n• Calcium supplements\n• Clean water daily",
        "uz": "🐦 <b>Qushlarni oziqlantirish:</b>\n\n• Maxsus don aralashmalari\n• Yangi mevalar va sabzavotlar\n• Kalsiy qo'shimchalari\n• Har kuni toza suv"
    }
}


# --- СОСТОЯНИЯ ДЛЯ FSM ---
class ProfileStates(StatesGroup):
    waiting_for_profile_type = State()
    waiting_for_owner_name = State()
    waiting_for_owner_phone = State()
    waiting_for_city = State()
    waiting_for_pet_name = State()
    waiting_for_pet_type = State()
    waiting_for_pet_breed = State()
    waiting_for_pet_age = State()
    waiting_for_pet_weight = State()
    waiting_for_pet_color = State()
    waiting_for_allergies = State()
    waiting_for_diseases = State()
    waiting_for_vaccinations = State()


class VetProfileStates(StatesGroup):
    waiting_for_vet_name = State()
    waiting_for_vet_phone = State()
    waiting_for_vet_city = State()
    waiting_for_vet_specialization = State()
    waiting_for_vet_experience = State()
    waiting_for_vet_education = State()
    waiting_for_vet_telegram = State()
    waiting_for_vet_consultation_price = State()
    waiting_for_vet_info = State()


class ReminderStates(StatesGroup):
    waiting_for_reminder_type = State()
    waiting_for_reminder_text = State()
    waiting_for_reminder_date = State()
    waiting_for_reminder_time = State()
    waiting_for_reminder_days = State()


class AdStates(StatesGroup):
    waiting_for_ad_title = State()
    waiting_for_ad_text = State()
    waiting_for_ad_price = State()
    waiting_for_ad_contact = State()


class SymptomsStates(StatesGroup):
    waiting_for_pet_type = State()
    waiting_for_symptoms = State()


class LanguageStates(StatesGroup):
    waiting_for_language = State()


# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========
def add_to_history(user_id, text):
    """Добавляет запись в историю пользователя"""
    if user_id not in user_history:
        user_history[user_id] = []

    timestamp = datetime.now().strftime("%d.%m %H:%M")
    user_history[user_id].append(f"[{timestamp}] {text}")

    if len(user_history[user_id]) > 50:
        user_history[user_id] = user_history[user_id][-50:]


def get_text(user_id: int, text_key: str, **kwargs) -> str:
    """Получить текст на нужном языке"""
    lang = user_languages.get(user_id, "ru")
    text_dict = TEXTS.get(text_key, {})
    text = text_dict.get(lang, text_dict.get("ru", text_key))

    if kwargs:
        text = text.format(**kwargs)

    return text


async def safe_edit_message(message, text, reply_markup=None, parse_mode=ParseMode.HTML):
    """Безопасное редактирование сообщения"""
    try:
        await message.edit_text(
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )
        return True
    except Exception:
        try:
            await message.answer(
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup
            )
            return False
        except Exception:
            return False


def create_reminder_keyboard():
    """Клавиатура для создания напоминаний"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏰ Один раз", callback_data="reminder_one_time")],
        [InlineKeyboardButton(text="🔄 Ежедневно", callback_data="reminder_daily")],
        [InlineKeyboardButton(text="📆 Еженедельно", callback_data="reminder_weekly")],
        [InlineKeyboardButton(text="⚙️ Настроить дни", callback_data="reminder_custom")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_reminders")]
    ])


def create_cities_keyboard():
    """Клавиатура с городами Узбекистана"""
    buttons = []
    row = []

    for i, city_key in enumerate(UZBEK_CITIES):
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
    """Клавиатура для выбора типа животного"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐕 Собака", callback_data="animal_dog")],
        [InlineKeyboardButton(text="🐱 Кошка", callback_data="animal_cat")],
        [InlineKeyboardButton(text="🐹 Грызуны", callback_data="animal_rodent")],
        [InlineKeyboardButton(text="🐦 Птицы", callback_data="animal_bird")],
        [InlineKeyboardButton(text="🐠 Рыбки", callback_data="animal_fish")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
    ])


def create_feeding_keyboard():
    """Клавиатура для выбора типа животного для кормления"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Домашние животные", callback_data="feeding_domestic")],
        [InlineKeyboardButton(text="🐄 Сельскохозяйственные", callback_data="feeding_farm")],
        [InlineKeyboardButton(text="🦎 Экзотические", callback_data="feeding_exotic")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
    ])


def create_domestic_animals_keyboard():
    """Клавиатура для выбора домашних животных"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐕 Собаки", callback_data="feed_dog")],
        [InlineKeyboardButton(text="🐱 Кошки", callback_data="feed_cat")],
        [InlineKeyboardButton(text="🐹 Грызуны", callback_data="feed_rodent")],
        [InlineKeyboardButton(text="🐦 Птицы", callback_data="feed_bird")],
        [InlineKeyboardButton(text="🐠 Рыбки", callback_data="feed_fish")],
        [InlineKeyboardButton(text="🐢 Рептилии", callback_data="feed_reptile")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu_feeding")]
    ])


def create_language_keyboard():
    """Клавиатура выбора языка"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
    ])


# ========== ФУНКЦИИ МЕНЮ ==========

def get_main_menu(user_id: int = None):
    """Главное меню на нужном языке с большой кнопкой профиля"""
    if user_id is None:
        lang = "ru"
    else:
        lang = user_languages.get(user_id, "ru")

    # Большая кнопка профиля (занимает всю ширину)
    menu_buttons = [
        [InlineKeyboardButton(
            text=get_text(user_id, "profile_big"),
            callback_data="menu_profile"
        )],
        [
            InlineKeyboardButton(text=get_text(user_id, "ads"), callback_data="menu_ads"),
            InlineKeyboardButton(text=get_text(user_id, "news"), callback_data="menu_news")
        ],
        [
            InlineKeyboardButton(text=get_text(user_id, "pet_shop"), callback_data="menu_pet_shop"),
            InlineKeyboardButton(text=get_text(user_id, "pet_facts"), callback_data="menu_facts")
        ],
        [
            InlineKeyboardButton(text=get_text(user_id, "feeding_guide"), callback_data="menu_feeding"),
            InlineKeyboardButton(text=get_text(user_id, "symptoms"), callback_data="menu_symptoms")
        ],
        [
            InlineKeyboardButton(text=get_text(user_id, "clinics"), callback_data="menu_clinics"),
            InlineKeyboardButton(text=get_text(user_id, "pharmacies"), callback_data="menu_pharmacies")
        ],
        [
            InlineKeyboardButton(text=get_text(user_id, "reminders"), callback_data="menu_reminders"),
            InlineKeyboardButton(text=get_text(user_id, "shelters"), callback_data="menu_shelters")
        ],
        [
            InlineKeyboardButton(text=get_text(user_id, "vet_chat"), callback_data="menu_vet_chat"),
            InlineKeyboardButton(text=get_text(user_id, "appointment"), callback_data="menu_appointment")
        ],
        [
            InlineKeyboardButton(text=get_text(user_id, "history"), callback_data="menu_history"),
            InlineKeyboardButton(text=get_text(user_id, "language"), callback_data="menu_language")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=menu_buttons)


def get_back_to_menu_button(user_id: int = None):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
    ])


def get_profile_menu(user_id: int = None):
    """Меню профиля с выбором типа профиля"""
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(user_id, "create_profile"), callback_data="create_profile")],
        [InlineKeyboardButton(text=get_text(user_id, "create_vet_profile"), callback_data="create_vet_profile")],
        [InlineKeyboardButton(text=get_text(user_id, "view_profile"), callback_data="profile_view")],
        [InlineKeyboardButton(text=get_text(user_id, "view_vet_profile"), callback_data="vet_profile_view")],
        [InlineKeyboardButton(text=get_text(user_id, "edit_profile"), callback_data="edit_profile")],
        [InlineKeyboardButton(text=get_text(user_id, "clear_profile"), callback_data="profile_clear")],
        [InlineKeyboardButton(text=get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
    ])
    return menu


def get_ads_menu(user_id: int = None):
    """Меню объявлений"""
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(user_id, "post_ad"), callback_data="post_ad")],
        [InlineKeyboardButton(text=get_text(user_id, "view_ads"), callback_data="view_ads")],
        [InlineKeyboardButton(text=get_text(user_id, "my_ads"), callback_data="my_ads")],
        [InlineKeyboardButton(text=get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
    ])
    return menu


def get_reminders_menu(user_id: int = None):
    """Меню напоминаний"""
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(user_id, "add_reminder"), callback_data="reminder_add")],
        [InlineKeyboardButton(text=get_text(user_id, "my_reminders"), callback_data="reminder_list")],
        [InlineKeyboardButton(text=get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
    ])
    return menu


# ========== ОБРАБОТЧИКИ КОМАНД ==========

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id

    # Инициализируем язык пользователя
    if user_id not in user_languages:
        user_languages[user_id] = "ru"

    # Инициализируем данные пользователя
    if user_id not in user_profiles:
        user_profiles[user_id] = {}
        user_symptoms[user_id] = []
        user_reminders[user_id] = []
        user_history[user_id] = []
        user_ads[user_id] = []
        appointments[user_id] = []
        add_to_history(user_id, "👋 Регистрация в боте")

    welcome_text = get_text(user_id, "welcome", name=message.from_user.first_name)

    await message.answer(
        text=welcome_text,
        reply_markup=get_main_menu(user_id)
    )


@dp.callback_query(F.data == "back_to_menu")
async def back_to_main_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "main_menu"),
        reply_markup=get_main_menu(user_id)
    )
    await callback.answer()


# ========== ПРОФИЛЬ ==========

@dp.callback_query(F.data == "menu_profile")
async def profile_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "profile_section"),
        reply_markup=get_profile_menu(user_id)
    )
    await callback.answer()


@dp.callback_query(F.data == "create_profile")
async def start_create_profile(callback: types.CallbackQuery, state: FSMContext):
    """Начало создания профиля владельца"""
    user_id = callback.from_user.id
    await state.set_state(ProfileStates.waiting_for_owner_name)

    await safe_edit_message(
        callback.message,
        "👤 <b>Создание профиля владельца</b>\n\n" + get_text(user_id, "enter_owner_name"),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )
    await callback.answer()


@dp.message(ProfileStates.waiting_for_owner_name)
async def process_owner_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(owner_name=message.text)
    await state.set_state(ProfileStates.waiting_for_owner_phone)

    await message.answer(
        get_text(user_id, "enter_owner_phone"),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@dp.message(ProfileStates.waiting_for_owner_phone)
async def process_owner_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(owner_phone=message.text)
    await state.set_state(ProfileStates.waiting_for_city)

    await message.answer(
        get_text(user_id, "enter_city"),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@dp.message(ProfileStates.waiting_for_city)
async def process_city(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(city=message.text)
    await state.set_state(ProfileStates.waiting_for_pet_name)

    await message.answer(
        get_text(user_id, "enter_pet_name"),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@dp.message(ProfileStates.waiting_for_pet_name)
async def process_pet_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(pet_name=message.text)
    await state.set_state(ProfileStates.waiting_for_pet_type)

    await message.answer(
        get_text(user_id, "enter_pet_type"),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@dp.message(ProfileStates.waiting_for_pet_type)
async def process_pet_type(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()

    # Сохраняем базовый профиль
    user_profiles[user_id] = {
        "owner_name": data.get('owner_name'),
        "owner_phone": data.get('owner_phone'),
        "city": data.get('city'),
        "pet_name": data.get('pet_name'),
        "pet_type": message.text,
        "created_at": datetime.now().strftime("%d.%m.%Y %H:%M")
    }

    add_to_history(user_id, "👤 Создан профиль владельца")
    await state.clear()

    # Показываем созданный профиль
    profile_text = (
        "✅ <b>Профиль успешно создан!</b>\n\n"
        f"👤 <b>Владелец:</b> {user_profiles[user_id]['owner_name']}\n"
        f"📞 <b>Телефон:</b> {user_profiles[user_id]['owner_phone']}\n"
        f"🌍 <b>Город:</b> {user_profiles[user_id]['city']}\n"
        f"🐾 <b>Питомец:</b> {user_profiles[user_id]['pet_name']}\n"
        f"📋 <b>Вид:</b> {user_profiles[user_id]['pet_type']}\n"
        f"📅 <b>Создан:</b> {user_profiles[user_id]['created_at']}"
    )

    await message.answer(
        profile_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_profile_menu(user_id)
    )


@dp.callback_query(F.data == "create_vet_profile")
async def start_create_vet_profile(callback: types.CallbackQuery, state: FSMContext):
    """Начало создания профиля ветеринара"""
    user_id = callback.from_user.id
    await state.set_state(VetProfileStates.waiting_for_vet_name)

    await safe_edit_message(
        callback.message,
        "👨‍⚕️ <b>Создание профиля ветеринара</b>\n\nВведите ваше полное имя:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )
    await callback.answer()


# Обработчики для профиля ветеринара
@dp.message(VetProfileStates.waiting_for_vet_name)
async def process_vet_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vet_name=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_phone)

    await message.answer(
        "📞 Введите ваш контактный телефон:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@dp.message(VetProfileStates.waiting_for_vet_phone)
async def process_vet_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vet_phone=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_city)

    await message.answer(
        "🏙️ Введите город, где вы работаете:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@dp.message(VetProfileStates.waiting_for_vet_city)
async def process_vet_city(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vet_city=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_specialization)

    await message.answer(
        "🎯 Введите вашу специализацию (например: хирург, терапевт, дерматолог):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@dp.message(VetProfileStates.waiting_for_vet_specialization)
async def process_vet_specialization(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vet_specialization=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_experience)

    await message.answer(
        "⏳ Введите ваш опыт работы (лет):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@dp.message(VetProfileStates.waiting_for_vet_experience)
async def process_vet_experience(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vet_experience=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_education)

    await message.answer(
        "🎓 Введите ваше образование:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@dp.message(VetProfileStates.waiting_for_vet_education)
async def process_vet_education(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vet_education=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_telegram)

    await message.answer(
        "💬 Введите ссылку на ваш Telegram аккаунт (например: @username):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@dp.message(VetProfileStates.waiting_for_vet_telegram)
async def process_vet_telegram(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vet_telegram=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_consultation_price)

    await message.answer(
        "💰 Введите стоимость консультации (например: 50$ или бесплатно):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@dp.message(VetProfileStates.waiting_for_vet_consultation_price)
async def process_vet_consultation_price(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vet_consultation_price=message.text)
    await state.set_state(VetProfileStates.waiting_for_vet_info)

    await message.answer(
        "📝 Напишите дополнительную информацию о себе и ваших услугах:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_profile")]
        ])
    )


@dp.message(VetProfileStates.waiting_for_vet_info)
async def process_vet_info(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.update_data(vet_info=message.text)

    # Сохраняем профиль ветеринара
    vet_profiles[user_id] = data
    add_to_history(user_id, "👨‍⚕️ Создан профиль ветеринара")
    await state.clear()

    # Формируем профиль для показа
    profile_text = (
        "👨‍⚕️ <b>ПРОФИЛЬ ВЕТЕРИНАРА</b>\n"
        "═════════════════════════\n"
        f"<b>👨 Имя:</b> {data.get('vet_name', '❌ Не указано')}\n"
        f"<b>📞 Телефон:</b> {data.get('vet_phone', '❌ Не указано')}\n"
        f"<b>🏙️ Город:</b> {data.get('vet_city', '❌ Не указано')}\n"
        f"<b>🎯 Специализация:</b> {data.get('vet_specialization', '❌ Не указано')}\n"
        f"<b>⏳ Опыт работы:</b> {data.get('vet_experience', '❌ Не указано')} лет\n"
        f"<b>🎓 Образование:</b> {data.get('vet_education', '❌ Не указано')}\n"
        f"<b>💬 Telegram:</b> {data.get('vet_telegram', '❌ Не указано')}\n"
        f"<b>💰 Консультация:</b> {data.get('vet_consultation_price', '❌ Не указано')}\n"
        f"<b>📝 О себе:</b>\n{data.get('vet_info', '❌ Не указано')}\n"
        "═════════════════════════"
    )

    await message.answer(
        "✅ <b>Профиль ветеринара успешно создан!</b>\n\n" + profile_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_profile_menu(user_id)
    )


@dp.callback_query(F.data == "profile_view")
async def view_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    profile = user_profiles.get(user_id, {})

    if not profile:
        text = get_text(user_id, "profile_empty")
        markup = get_profile_menu(user_id)
    else:
        # Формируем текст профиля владельца
        text = (
            "👤 <b>ВАШ ПРОФИЛЬ</b>\n"
            "════════════════════\n"
            f"<b>👨 Владелец:</b> {profile.get('owner_name', '❌ Не указано')}\n"
            f"<b>📞 Телефон:</b> {profile.get('owner_phone', '❌ Не указано')}\n"
            f"<b>🌍 Город:</b> {profile.get('city', '❌ Не указано')}\n\n"
            f"<b>🐾 Питомец:</b> {profile.get('pet_name', '❌ Не указано')}\n"
            f"<b>📋 Вид:</b> {profile.get('pet_type', '❌ Не указано')}\n"
            f"<b>📅 Создан:</b> {profile.get('created_at', '❌ Не указано')}\n"
            "════════════════════"
        )
        markup = get_profile_menu(user_id)

    await safe_edit_message(callback.message, text, reply_markup=markup)
    await callback.answer()


@dp.callback_query(F.data == "vet_profile_view")
async def view_vet_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    profile = vet_profiles.get(user_id, {})

    if not profile:
        text = get_text(user_id, "vet_profile_empty")
        markup = get_profile_menu(user_id)
    else:
        # Формируем текст профиля ветеринара
        text = (
            "👨‍⚕️ <b>ПРОФИЛЬ ВЕТЕРИНАРА</b>\n"
            "═════════════════════════\n"
            f"<b>👨 Имя:</b> {profile.get('vet_name', '❌ Не указано')}\n"
            f"<b>📞 Телефон:</b> {profile.get('vet_phone', '❌ Не указано')}\n"
            f"<b>🏙️ Город:</b> {profile.get('vet_city', '❌ Не указано')}\n"
            f"<b>🎯 Специализация:</b> {profile.get('vet_specialization', '❌ Не указано')}\n"
            f"<b>⏳ Опыт работы:</b> {profile.get('vet_experience', '❌ Не указано')} лет\n"
            f"<b>🎓 Образование:</b> {profile.get('vet_education', '❌ Не указано')}\n"
            f"<b>💬 Telegram:</b> {profile.get('vet_telegram', '❌ Не указано')}\n"
            f"<b>💰 Консультация:</b> {profile.get('vet_consultation_price', '❌ Не указано')}\n"
            f"<b>📝 О себе:</b>\n{profile.get('vet_info', '❌ Не указано')}\n"
            "═════════════════════════"
        )
        markup = get_profile_menu(user_id)

    await safe_edit_message(callback.message, text, reply_markup=markup)
    await callback.answer()


@dp.callback_query(F.data == "profile_clear")
async def clear_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_profiles[user_id] = {}
    vet_profiles[user_id] = {}
    add_to_history(user_id, "🗑️ Профиль очищен")

    await callback.answer("✅ Профиль очищен!")
    await back_to_main_menu(callback)


# ========== КЛИНИКИ И АПТЕКИ ==========

@dp.callback_query(F.data == "menu_clinics")
async def clinics_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "clinics_section"),
        reply_markup=create_cities_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "menu_pharmacies")
async def pharmacies_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "pharmacies_section"),
        reply_markup=create_cities_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("city_"))
async def show_city_info(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    city_key = callback.data.replace("city_", "")
    city_name = TEXTS.get(city_key, {}).get("ru", city_key)

    # Определяем тип запроса (клиники, аптеки или приюты)
    if "клиник" in callback.message.text.lower() or "clinic" in callback.message.text.lower():
        data = CLINICS_DATA.get(city_key, [f"🏥 В городе {city_name} информация о клиниках обновляется"])
        title = f"🏥 <b>Ветеринарные клиники в {city_name}:</b>\n\n"
    elif "аптек" in callback.message.text.lower() or "pharmacy" in callback.message.text.lower():
        data = PHARMACIES_DATA.get(city_key, [f"💊 В городе {city_name} информация об аптеках обновляется"])
        title = f"💊 <b>Ветеринарные аптеки в {city_name}:</b>\n\n"
    else:
        data = SHELTERS_DATA.get(city_key, [f"🏠 В городе {city_name} информация о приютах обновляется"])
        title = f"🏠 <b>Приюты для животных в {city_name}:</b>\n\n"

    text = title + "\n\n".join(data)

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📍 Показать на карте", callback_data=f"show_on_map_{city_key}")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("show_on_map_"))
async def show_on_map(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    city_key = callback.data.replace("show_on_map_", "")
    city_name = TEXTS.get(city_key, {}).get("ru", city_key)

    # Создаем ссылку на Google Maps для города
    maps_url = f"https://www.google.com/maps/search/ветеринарные+клиники+{city_name}"

    await callback.message.answer(
        f"📍 <b>{city_name} на карте</b>\n\n"
        f"Нажмите на ссылку ниже, чтобы открыть карту:\n"
        f"{maps_url}",
        parse_mode=ParseMode.HTML
    )
    await callback.answer()


# ========== НАПОМИНАНИЯ ==========

@dp.callback_query(F.data == "menu_reminders")
async def reminders_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "reminders_section"),
        reply_markup=get_reminders_menu(user_id)
    )
    await callback.answer()


@dp.callback_query(F.data == "reminder_add")
async def add_reminder(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.set_state(ReminderStates.waiting_for_reminder_type)

    await safe_edit_message(
        callback.message,
        get_text(user_id, "reminder_types"),
        reply_markup=create_reminder_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("reminder_"))
async def process_reminder_type(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    reminder_type = callback.data

    await state.update_data(reminder_type=reminder_type)
    await state.set_state(ReminderStates.waiting_for_reminder_text)

    await safe_edit_message(
        callback.message,
        "📝 Введите текст напоминания (например: 'Дать лекарство коту', 'Вакцинация собаки'):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_reminders")]
        ])
    )
    await callback.answer()


@dp.message(ReminderStates.waiting_for_reminder_text)
async def process_reminder_text(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    reminder_type = data.get('reminder_type')

    await state.update_data(reminder_text=message.text)

    if reminder_type == "reminder_one_time":
        await state.set_state(ReminderStates.waiting_for_reminder_date)
        await message.answer(
            "📅 Введите дату напоминания (в формате ДД.ММ.ГГГГ, например: 25.12.2024):",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_reminders")]
            ])
        )
    elif reminder_type == "reminder_daily":
        await state.set_state(ReminderStates.waiting_for_reminder_time)
        await message.answer(
            "⏰ Введите время напоминания (в формате ЧЧ:ММ, например: 09:00):",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_reminders")]
            ])
        )
    elif reminder_type == "reminder_weekly":
        await state.set_state(ReminderStates.waiting_for_reminder_days)
        await message.answer(
            "📆 Введите дни недели для напоминания (например: ПН,СР,ПТ или понедельник,среда,пятница):",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_reminders")]
            ])
        )
    else:
        await state.set_state(ReminderStates.waiting_for_reminder_date)
        await message.answer(
            "📅 Введите даты напоминаний через запятую (в формате ДД.ММ.ГГГГ):",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_reminders")]
            ])
        )


@dp.message(ReminderStates.waiting_for_reminder_date)
async def process_reminder_date(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()

    reminder = {
        "text": data.get('reminder_text'),
        "type": data.get('reminder_type'),
        "date": message.text,
        "created": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "active": True
    }

    if user_id not in user_reminders:
        user_reminders[user_id] = []

    user_reminders[user_id].append(reminder)
    add_to_history(user_id, f"⏰ Добавлено напоминание: {reminder['text']}")

    await state.clear()

    await message.answer(
        f"✅ <b>Напоминание добавлено!</b>\n\n"
        f"<b>Текст:</b> {reminder['text']}\n"
        f"<b>Дата:</b> {reminder['date']}\n"
        f"<b>Тип:</b> {'Один раз' if reminder['type'] == 'reminder_one_time' else 'Настроенное'}\n\n"
        f"Я напомню вам в указанное время!",
        parse_mode=ParseMode.HTML,
        reply_markup=get_reminders_menu(user_id)
    )


@dp.callback_query(F.data == "reminder_list")
async def show_reminders(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    reminders = user_reminders.get(user_id, [])

    if not reminders:
        text = "📭 <b>У вас нет активных напоминаний</b>"
    else:
        text = "📋 <b>Ваши напоминания:</b>\n\n"
        for i, reminder in enumerate(reminders, 1):
            text += f"{i}. <b>{reminder['text']}</b>\n"
            text += f"   📅 {reminder['date']}\n"
            text += f"   🕒 Создано: {reminder['created']}\n\n"

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=get_reminders_menu(user_id)
    )
    await callback.answer()


# ========== ПРИЮТЫ ==========

@dp.callback_query(F.data == "menu_shelters")
async def shelters_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "shelters_section"),
        reply_markup=create_cities_keyboard()
    )
    await callback.answer()


# ========== ОБЪЯВЛЕНИЯ ==========

@dp.callback_query(F.data == "menu_ads")
async def ads_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "ads_section"),
        reply_markup=get_ads_menu(user_id)
    )
    await callback.answer()


@dp.callback_query(F.data == "post_ad")
async def post_ad(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.set_state(AdStates.waiting_for_ad_title)

    await safe_edit_message(
        callback.message,
        "📝 <b>Создание объявления</b>\n\nВведите заголовок объявления:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_ads")]
        ])
    )
    await callback.answer()


@dp.message(AdStates.waiting_for_ad_title)
async def process_ad_title(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(ad_title=message.text)
    await state.set_state(AdStates.waiting_for_ad_text)

    await message.answer(
        "📄 Введите текст объявления:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_ads")]
        ])
    )


@dp.message(AdStates.waiting_for_ad_text)
async def process_ad_text(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(ad_text=message.text)
    await state.set_state(AdStates.waiting_for_ad_price)

    await message.answer(
        "💰 Введите цену (или 'Бесплатно', 'Договорная'):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_ads")]
        ])
    )


@dp.message(AdStates.waiting_for_ad_price)
async def process_ad_price(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(ad_price=message.text)
    await state.set_state(AdStates.waiting_for_ad_contact)

    await message.answer(
        "📞 Введите контактную информацию (телефон или Telegram):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_ads")]
        ])
    )


@dp.message(AdStates.waiting_for_ad_contact)
async def process_ad_contact(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()

    ad = {
        "title": data.get('ad_title'),
        "text": data.get('ad_text'),
        "price": data.get('ad_price'),
        "contact": message.text,
        "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "user_id": user_id
    }

    if user_id not in user_ads:
        user_ads[user_id] = []

    user_ads[user_id].append(ad)
    add_to_history(user_id, f"📢 Добавлено объявление: {ad['title']}")

    await state.clear()

    ad_text = (
        f"✅ <b>Объявление опубликовано!</b>\n\n"
        f"<b>Заголовок:</b> {ad['title']}\n"
        f"<b>Описание:</b> {ad['text']}\n"
        f"<b>Цена:</b> {ad['price']}\n"
        f"<b>Контакты:</b> {ad['contact']}\n"
        f"<b>Дата:</b> {ad['date']}"
    )

    await message.answer(
        ad_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_ads_menu(user_id)
    )


@dp.callback_query(F.data == "my_ads")
async def show_my_ads(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    ads = user_ads.get(user_id, [])

    if not ads:
        text = "📭 <b>У вас нет опубликованных объявлений</b>"
    else:
        text = "📋 <b>Ваши объявления:</b>\n\n"
        for i, ad in enumerate(ads, 1):
            text += f"{i}. <b>{ad['title']}</b>\n"
            text += f"   💰 {ad['price']}\n"
            text += f"   📅 {ad['date']}\n"
            text += f"   👁️ {ad['contact']}\n\n"

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=get_ads_menu(user_id)
    )
    await callback.answer()


# ========== НОВОСТИ ==========

@dp.callback_query(F.data == "menu_news")
async def news_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    # Пример новостей
    news_list = [
        "📰 <b>Новость 1:</b> В Ташкенте открылся новый приют для бездомных животных",
        "📰 <b>Новость 2:</b> Бесплатная вакцинация собак от бешенства в Самарканде",
        "📰 <b>Новость 3:</b> Конкурс на лучший зоомагазин Узбекистана 2024",
        "📰 <b>Новость 4:</b> Новый закон о защите животных в Узбекистане"
    ]

    text = get_text(user_id, "news_section") + "\n\n" + "\n\n".join(news_list)

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Обновить новости", callback_data="menu_news")],
            [InlineKeyboardButton(text=get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


# ========== ИНТЕРЕСНЫЕ ФАКТЫ ==========

@dp.callback_query(F.data == "menu_facts")
async def facts_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    import random
    random_fact = random.choice(ANIMAL_FACTS)

    text = get_text(user_id, "facts_section") + f"\n\n🎲 <b>Случайный факт:</b>\n\n{random_fact}"

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎲 Еще факт", callback_data="menu_facts")],
            [InlineKeyboardButton(text=get_text(user_id, "back_to_menu"), callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


# ========== КОРМЛЕНИЕ ==========

@dp.callback_query(F.data == "menu_feeding")
async def feeding_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "feeding_section"),
        reply_markup=create_feeding_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "feeding_domestic")
async def domestic_feeding(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        "🏠 <b>Кормление домашних животных</b>\n\nВыберите тип животного:",
        reply_markup=create_domestic_animals_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("feed_"))
async def show_feeding_info(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    animal_type = callback.data.replace("feed_", "")

    info = FEEDING_INFO.get(animal_type, {}).get(user_languages.get(user_id, "ru"), "Информация обновляется...")

    await safe_edit_message(
        callback.message,
        info,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="feeding_domestic")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


# ========== СИМПТОМЫ ==========

@dp.callback_query(F.data == "menu_symptoms")
async def symptoms_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "symptoms_section"),
        reply_markup=create_animal_type_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("animal_"))
async def process_animal_type(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    animal_type = callback.data.replace("animal_", "")

    await state.update_data(pet_type=animal_type)
    await state.set_state(SymptomsStates.waiting_for_symptoms)

    animal_names = {
        "dog": "собаки",
        "cat": "кошки",
        "rodent": "грызуна",
        "bird": "птицы",
        "fish": "рыбок"
    }

    animal_name = animal_names.get(animal_type, "животного")

    await safe_edit_message(
        callback.message,
        f"🩺 <b>Проверка симптомов у {animal_name}</b>\n\n"
        f"Опишите симптомы вашего питомца (что вас беспокоит, как давно, дополнительные детали):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="menu_symptoms")]
        ])
    )
    await callback.answer()


@dp.message(SymptomsStates.waiting_for_symptoms)
async def process_symptoms(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()

    symptoms_text = message.text
    pet_type = data.get('pet_type', 'неизвестно')

    # Сохраняем симптомы
    if user_id not in user_symptoms:
        user_symptoms[user_id] = []

    symptom_record = {
        "pet_type": pet_type,
        "symptoms": symptoms_text,
        "date": datetime.now().strftime("%d.%m.%Y %H:%M")
    }

    user_symptoms[user_id].append(symptom_record)
    add_to_history(user_id, f"🩺 Добавлены симптомы: {symptoms_text[:50]}...")

    # Простой анализ симптомов
    response = "🩺 <b>Рекомендации по симптомам:</b>\n\n"

    # Базовая логика анализа
    if any(word in symptoms_text.lower() for word in ['рвота', 'понос', 'диарея']):
        response += "⚠️ <b>Симптомы могут указывать на отравление или инфекцию.</b>\n"
        response += "• Обеспечьте доступ к воде\n"
        response += "• Не кормите 12-24 часа\n"
        response += "• Срочно обратитесь к ветеринару\n\n"
    elif any(word in symptoms_text.lower() for word in ['не ест', 'аппетит', 'отказ']):
        response += "⚠️ <b>Отказ от еды может быть признаком различных заболеваний.</b>\n"
        response += "• Проверьте температуру\n"
        response += "• Предложите любимое лакомство\n"
        response += "• Если не ест более 24 часов - к врачу\n\n"
    elif any(word in symptoms_text.lower() for word in ['чешется', 'зуд', 'аллергия']):
        response += "⚠️ <b>Возможна аллергия или кожное заболевание.</b>\n"
        response += "• Проверьте на блох и клещей\n"
        response += "• Исключите новые продукты\n"
        response += "• Консультация дерматолога\n\n"
    else:
        response += "ℹ️ <b>Общие рекомендации:</b>\n"
        response += "• Наблюдайте за состоянием\n"
        response += "• Измерьте температуру\n"
        response += "• При ухудшении - обратитесь к ветеринару\n\n"

    response += f"<b>📝 Ваши симптомы сохранены:</b>\n{symptoms_text}\n\n"
    response += "<b>⚠️ ВНИМАНИЕ:</b> Это только рекомендации. Для точного диагноза обратитесь к ветеринару!"

    await state.clear()

    await message.answer(
        response,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📍 Найти клинику", callback_data="menu_clinics")],
            [InlineKeyboardButton(text="💬 Чат с ветер.", callback_data="menu_vet_chat")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")]
        ])
    )


# ========== ЯЗЫК ==========

@dp.callback_query(F.data == "menu_language")
async def language_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        get_text(user_id, "choose_language"),
        reply_markup=create_language_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("lang_"))
async def set_language(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    language = callback.data.replace("lang_", "")

    user_languages[user_id] = language
    add_to_history(user_id, f"🌍 Изменен язык на {language}")

    languages = {
        "ru": "🇷🇺 Русский",
        "uz": "🇺🇿 O'zbekcha"
    }

    await callback.answer(f"Язык изменен на {languages.get(language, language)}!")
    await back_to_main_menu(callback)


# ========== ИСТОРИЯ ==========

@dp.callback_query(F.data == "menu_history")
async def history_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    history = user_history.get(user_id, [])

    if not history:
        text = "📭 <b>История пуста</b>\n\nЗдесь будут отображаться ваши действия в боте."
    else:
        text = "📋 <b>История действий:</b>\n\n"
        for record in history[-10:]:  # Последние 10 записей
            text += f"• {record}\n"

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑️ Очистить историю", callback_data="clear_history")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


@dp.callback_query(F.data == "clear_history")
async def clear_history(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_history[user_id] = []
    add_to_history(user_id, "🗑️ История очищена")

    await callback.answer("✅ История очищена!")
    await history_menu(callback)


# ========== MINI APP ==========

@dp.callback_query(F.data == "menu_mini_app")
async def mini_app_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    # Пример Mini App (можно заменить на реальный URL)
    web_app = WebAppInfo(url="https://example.com/pet-helper-app")

    await callback.message.answer(
        "📱 <b>PetHelper Mini App</b>\n\n"
        "Откройте наше мини-приложение для дополнительных функций:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Открыть Mini App", web_app=web_app)],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


# ========== ДОПОЛНИТЕЛЬНЫЕ МЕНЮ ==========

@dp.callback_query(F.data == "menu_pet_shop")
async def pet_shop_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    text = get_text(user_id, "pet_shop_section")

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=create_cities_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "menu_vet_chat")
async def vet_chat_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    # Проверяем, есть ли ветеринары
    available_vets = [vet for vet_id, vet in vet_profiles.items() if vet_id != user_id]

    if not available_vets:
        text = "💬 <b>Чат с ветеринаром</b>\n\n"
        text += "К сожалению, в данный момент нет доступных ветеринаров онлайн.\n"
        text += "Вы можете:\n"
        text += "• Найти клинику для очного приема\n"
        text += "• Создать профиль ветеринара, если вы специалист"

        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📍 Клиники", callback_data="menu_clinics")],
            [InlineKeyboardButton(text="👨‍⚕️ Стать ветер.", callback_data="create_vet_profile")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ])
    else:
        text = get_text(user_id, "vet_chat_section")

        buttons = []
        for vet in available_vets[:5]:  # Максимум 5 ветеринаров
            vet_name = vet.get('vet_name', 'Ветеринар')
            vet_spec = vet.get('vet_specialization', 'Специалист')
            buttons.append([InlineKeyboardButton(
                text=f"👨‍⚕️ {vet_name} ({vet_spec})",
                callback_data=f"chat_with_{list(vet_profiles.keys())[list(vet_profiles.values()).index(vet)]}"
            )])

        buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")])
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    await safe_edit_message(callback.message, text, reply_markup=markup)
    await callback.answer()


@dp.callback_query(F.data == "menu_appointment")
async def appointment_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    text = get_text(user_id, "appointment_section")

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📅 Записаться онлайн", callback_data="book_appointment")],
            [InlineKeyboardButton(text="📍 Найти клинику", callback_data="menu_clinics")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()


# ========== ЗАПУСК БОТА ==========

async def main():
    print("=" * 50)
    print("🐾 ВЕТЕРИНАРНЫЙ БОТ PETHELPER ЗАПУСКАЕТСЯ...")
    print("✅ Версия: 2.0 (Полностью рабочий код)")
    print("✅ Функции:")
    print("   • Мультиязычный интерфейс (RU/EN/UZ)")
    print("   • Профили владельцев и ветеринаров")
    print("   • Поиск клиник, аптек, приютов")
    print("   • Система напоминаний")
    print("   • Объявления и новости")
    print("   • Интересные факты о животных")
    print("   • Рекомендации по кормлению")
    print("   • Проверка симптомов")
    print("   • История действий")
    print("   • Поддержка Mini App")
    print("=" * 50)

    # Удаляем вебхук перед запуском
    try:
        print("Удаляю вебхук...")
        await bot.delete_webhook(drop_pending_updates=True)
        print("✅ Вебхук удален!")
    except Exception as e:
        print(f"⚠️ Ошибка при удалении вебхука: {e}")

    # Запускаем бота
    print("Запускаю бота...")
    print("✅ Бот готов к работе!")
    print("👉 Напишите /start в Telegram")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    # Установите нужные библиотеки: pip install aiogram python-dotenv
    asyncio.run(main())
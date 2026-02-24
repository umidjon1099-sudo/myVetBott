"""Static bot texts and reference data."""

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
        "ru": "🌍 Язык",
        "en": "🌍 Language",
        "uz": "🌍 Til"
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


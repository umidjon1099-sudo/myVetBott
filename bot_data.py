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
        "ru": "🦴 Кормление питомца",
        "en": "🦴 Feeding Guide",
        "uz": "🦴 Hayvonni oziqlantirish"
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
    "clinics_shelters": {
        "ru": "🏥 Клиники + 🏠 Приюты",
        "en": "🏥 Clinics + 🏠 Shelters",
        "uz": "🏥 Klinikalar + 🏠 Boshpanalar"
    },
    "pharmacies_pet_shop": {
        "ru": "💊 Аптеки + 🛒 Зоомагазин",
        "en": "💊 Pharmacies + 🛒 Pet Shop",
        "uz": "💊 Dorixonalar + 🛒 Pet shop"
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
        "en": "📅 Appointment",
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
        "ru": "👤 <b>Мой профиль</b>\n\nВыберите раздел:",
        "en": "👤 <b>My Profile</b>\n\nChoose a section:",
        "uz": "👤 <b>Mening profilim</b>\n\nBo'limni tanlang:"
    },
    "create_profile": {
        "ru": "✍️ Создать профиль",
        "en": "✍️ Create Profile",
        "uz": "✍️ Profil yaratish"
    },
    "view_profile": {
        "ru": "👁️ Посмотреть профиль",
        "en": "👁️ View Profile",
        "uz": "👁️ Profilni ko'rish"
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

# Интересные факты о животных (RU/EN/UZ)
ANIMAL_FACTS = {
    "ru": [
        "🐕 Собаки понимают до 250 слов и жестов.",
        "🐱 Кошки спят около 70% своей жизни.",
        "🐰 Кролики могут видеть позади себя, не поворачивая головы.",
        "🐦 Попугаи могут жить более 80 лет.",
        "🐠 Золотые рыбки способны запоминать информацию на месяцы.",
        "🦜 Некоторые попугаи умеют очень точно копировать человеческую речь.",
        "🐹 Хомяк за ночь может пробежать несколько километров в колесе.",
        "🐢 Некоторые черепахи живут более 100 лет.",
        "🦎 Ряд ящериц может сбрасывать хвост при опасности.",
        "🐭 Мыши издают ультразвуковые сигналы, похожие на смех.",
        "🐶 Отпечаток носа у собаки уникален, как отпечаток пальца у человека.",
        "🐱 У кошек около 30 мышц управляют движением ушей.",
        "🦉 Совы могут поворачивать голову примерно на 270 градусов.",
        "🐙 У осьминога три сердца.",
        "🐝 Пчёлы сообщают о местонахождении еды с помощью «танца».",
        "🦒 Язык жирафа может достигать примерно 45 см.",
        "🐬 Дельфины узнают себя в зеркале.",
        "🦈 Акулы существовали раньше динозавров.",
        "🐧 Императорские пингвины могут нырять глубже 500 метров.",
        "🦋 Бабочки чувствуют вкус лапками.",
        "🐘 Слоны узнают друг друга по голосу на больших расстояниях.",
        "🐸 Некоторые лягушки могут замерзать и потом «оживать».",
        "🦦 Выдры держатся за лапы во сне, чтобы не уплыть друг от друга.",
        "🐎 Лошади могут спать как стоя, так и лёжа.",
        "🦔 Ежи плохо видят, но отлично чувствуют запахи.",
    ],
    "en": [
        "🐕 Dogs can understand up to 250 words and gestures.",
        "🐱 Cats sleep about 70% of their lives.",
        "🐰 Rabbits can see behind themselves without turning their heads.",
        "🐦 Parrots can live more than 80 years.",
        "🐠 Goldfish can remember information for months.",
        "🦜 Some parrots can mimic human speech very accurately.",
        "🐹 A hamster can run several kilometers in a wheel overnight.",
        "🐢 Some turtles can live over 100 years.",
        "🦎 Many lizards can drop their tails when threatened.",
        "🐭 Mice make ultrasonic sounds that resemble laughter.",
        "🐶 A dog's nose print is unique, like a human fingerprint.",
        "🐱 Cats use around 30 muscles to move their ears.",
        "🦉 Owls can rotate their heads about 270 degrees.",
        "🐙 An octopus has three hearts.",
        "🐝 Bees communicate food locations through a dance.",
        "🦒 A giraffe's tongue can be about 45 cm long.",
        "🐬 Dolphins can recognize themselves in mirrors.",
        "🦈 Sharks existed before dinosaurs.",
        "🐧 Emperor penguins can dive deeper than 500 meters.",
        "🦋 Butterflies taste with their feet.",
        "🐘 Elephants can recognize each other by voice over long distances.",
        "🐸 Some frogs can freeze and later thaw back to life.",
        "🦦 Otters hold hands while sleeping so they do not drift apart.",
        "🐎 Horses can sleep standing up and lying down.",
        "🦔 Hedgehogs have poor eyesight but a strong sense of smell.",
    ],
    "uz": [
        "🐕 Itlar 250 tagacha so'z va imo-ishorani tushunishi mumkin.",
        "🐱 Mushuklar hayotining taxminan 70% qismini uyquda o'tkazadi.",
        "🐰 Quyonlar boshini burmasdan ham orqa tomonni ko'ra oladi.",
        "🐦 To'tiqushlar 80 yildan ortiq yashashi mumkin.",
        "🐠 Oltin baliqlar ma'lumotni oylar davomida eslab qolishi mumkin.",
        "🦜 Ba'zi to'tiqushlar inson nutqini juda aniq taqlid qiladi.",
        "🐹 Xomyak bir kechada g'ildirakda bir necha km yugurishi mumkin.",
        "🐢 Ba'zi toshbaqalar 100 yildan ortiq yashaydi.",
        "🦎 Ko'plab kaltakesaklar xavf paytida dumini tashlab yubora oladi.",
        "🐭 Sichqonlar kulgiga o'xshash ultratovush signallar chiqaradi.",
        "🐶 It burni izi inson barmoq izi kabi noyob bo'ladi.",
        "🐱 Mushuk quloqlarini boshqarish uchun taxminan 30 ta mushakdan foydalanadi.",
        "🦉 Boyqushlar boshini taxminan 270 gradusga burishi mumkin.",
        "🐙 Sakkizoyoqda uchta yurak bor.",
        "🐝 Asalarilar ozuqa joyini raqs orqali ko'rsatadi.",
        "🦒 Jirafaning tili taxminan 45 sm bo'lishi mumkin.",
        "🐬 Delfinlar oynada o'zini taniy oladi.",
        "🦈 Akulalar dinozavrlardan ham oldin mavjud bo'lgan.",
        "🐧 Imperator pingvinlari 500 metrdan chuqur sho'ng'iy oladi.",
        "🦋 Kapalaklar ta'mni oyoqlari bilan sezadi.",
        "🐘 Fillar uzoq masofadan bir-birini ovozi orqali taniydi.",
        "🐸 Ba'zi qurbaqalar muzlab, keyin yana tirik holatga qayta oladi.",
        "🦦 Suv suvsarlari uxlaganda bir-birining panjasini ushlab yotadi.",
        "🐎 Otlar tik turgan holda ham, yotgan holda ham uxlashi mumkin.",
        "🦔 Tipratikanlarning ko'rishi sust, lekin hid bilishi kuchli.",
    ],
}

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

# Симптомы по видам животных (мультиязычные названия и причины)
SYMPTOM_ANIMALS = {
    "dog": {
        "emoji": "🐕",
        "name": {"ru": "Собаки", "en": "Dogs", "uz": "Itlar"},
    },
    "cat": {
        "emoji": "🐱",
        "name": {"ru": "Кошки", "en": "Cats", "uz": "Mushuklar"},
    },
    "cow": {
        "emoji": "🐄",
        "name": {"ru": "Коровы", "en": "Cows", "uz": "Sigirlar"},
    },
    "sheep": {
        "emoji": "🐏",
        "name": {"ru": "Бараны / Овцы", "en": "Rams / Sheep", "uz": "Qo'y / Qo'chqor"},
    },
    "rodent": {
        "emoji": "🐹",
        "name": {"ru": "Грызуны", "en": "Rodents", "uz": "Kemiruvchilar"},
    },
    "bird": {
        "emoji": "🐦",
        "name": {"ru": "Птицы", "en": "Birds", "uz": "Qushlar"},
    },
    "fish": {
        "emoji": "🐠",
        "name": {"ru": "Рыбки", "en": "Fish", "uz": "Baliqlar"},
    },
    "exotic": {
        "emoji": "🦎",
        "name": {"ru": "Экзотические", "en": "Exotic Pets", "uz": "Ekzotik hayvonlar"},
    },
}

SYMPTOM_LIBRARY = {
    "dog": [
        {
            "title": {
                "ru": "😴 Вялость / слабость",
                "en": "😴 Lethargy / weakness",
                "uz": "😴 Loqaydlik / holsizlik",
            },
            "causes": {
                "ru": ["Лихорадка", "Боль", "Интоксикация", "Анемия", "Сердечная недостаточность", "Эндокринные нарушения"],
                "en": ["Fever", "Pain", "Intoxication", "Anemia", "Heart failure", "Endocrine disorders"],
                "uz": ["Isitma", "Og'riq", "Zaharlanish", "Anemiya", "Yurak yetishmovchiligi", "Endokrin buzilishlar"],
            },
            "emergency": False,
        },
        {
            "title": {"ru": "🍽️ Отказ от корма / анорексия", "en": "🍽️ Food refusal / anorexia", "uz": "🍽️ Ozuqadan voz kechish / anoreksiya"},
            "causes": {
                "ru": ["Заболевания ЖКТ", "Заболевания печени", "Панкреатит", "Стоматологическая боль", "Инфекции", "Стресс / боль"],
                "en": ["GI diseases", "Liver diseases", "Pancreatitis", "Dental pain", "Infections", "Stress / pain"],
                "uz": ["OVT kasalliklari", "Jigar kasalliklari", "Pankreatit", "Tish og'rig'i", "Infeksiyalar", "Stress / og'riq"],
            },
            "emergency": False,
        },
        {
            "title": {"ru": "🤮 Рвота", "en": "🤮 Vomiting", "uz": "🤮 Qusish"},
            "causes": {
                "ru": ["Гастрит / гастроэнтерит", "Инородное тело", "Отравление", "Панкреатит", "Заболевания печени", "Почечная недостаточность"],
                "en": ["Gastritis / gastroenteritis", "Foreign body", "Poisoning", "Pancreatitis", "Liver disease", "Kidney failure"],
                "uz": ["Gastrit / gastroenterit", "Yot jism", "Zaharlanish", "Pankreatit", "Jigar kasalliklari", "Buyrak yetishmovchiligi"],
            },
            "emergency": False,
        },
        {
            "title": {"ru": "💩 Диарея", "en": "💩 Diarrhea", "uz": "💩 Ich ketishi"},
            "causes": {
                "ru": ["Паразиты", "Бактериальные / вирусные инфекции", "Пищевая непереносимость", "Воспалительные заболевания кишечника", "Интоксикация"],
                "en": ["Parasites", "Bacterial / viral infections", "Food intolerance", "Inflammatory bowel disease", "Intoxication"],
                "uz": ["Parazitlar", "Bakterial / virusli infeksiyalar", "Ozuqa intoleransi", "Ichak yallig'lanish kasalliklari", "Intoksikatsiya"],
            },
            "emergency": False,
        },
        {
            "title": {"ru": "😮‍💨 Одышка / учащённое дыхание", "en": "😮‍💨 Shortness of breath / rapid breathing", "uz": "😮‍💨 Hansirash / tez nafas olish"},
            "causes": {
                "ru": ["Сердечная недостаточность", "Отёк лёгких", "Тепловой удар", "Плевральный выпот", "Сильная боль"],
                "en": ["Heart failure", "Pulmonary edema", "Heat stroke", "Pleural effusion", "Severe pain"],
                "uz": ["Yurak yetishmovchiligi", "O'pka shishi", "Issiq urishi", "Plevral suyuqlik", "Kuchli og'riq"],
            },
            "emergency": True,
        },
        {
            "title": {"ru": "🤕 Хромота", "en": "🤕 Lameness", "uz": "🤕 Oqsoqlik"},
            "causes": {"ru": ["Травмы", "Разрывы связок", "Артрит / остеоартроз", "Дисплазии", "Неврологические нарушения"], "en": ["Injuries", "Ligament tears", "Arthritis / osteoarthritis", "Dysplasia", "Neurological disorders"], "uz": ["Jarohatlar", "Bog'lam uzilishi", "Artrit / osteoartroz", "Displaziya", "Nevrologik buzilishlar"]},
            "emergency": False,
        },
        {
            "title": {"ru": "⚡ Судороги", "en": "⚡ Seizures", "uz": "⚡ Tutqanoq"},
            "causes": {"ru": ["Эпилепсия", "Интоксикация", "Гипогликемия", "Печёночная энцефалопатия", "Травма ЦНС"], "en": ["Epilepsy", "Intoxication", "Hypoglycemia", "Hepatic encephalopathy", "CNS trauma"], "uz": ["Epilepsiya", "Intoksikatsiya", "Gipoglikemiya", "Jigar ensefalopatiyasi", "MNS jarohati"]},
            "emergency": True,
        },
    ],
    "cat": [
        {"title": {"ru": "😴 Вялость / скрытность", "en": "😴 Lethargy / hiding", "uz": "😴 Loqaydlik / yashirinib yurish"}, "causes": {"ru": ["Вирусные инфекции", "Боль", "Заболевания почек", "Анемия", "Сердечные заболевания"], "en": ["Viral infections", "Pain", "Kidney disease", "Anemia", "Heart disease"], "uz": ["Virusli infeksiyalar", "Og'riq", "Buyrak kasalliklari", "Anemiya", "Yurak kasalliklari"]}, "emergency": False},
        {"title": {"ru": "🍽️ Отказ от еды (более 24 ч — опасно)", "en": "🍽️ Food refusal (over 24h is dangerous)", "uz": "🍽️ Ovqat yemaydi (24 soatdan ortiq xavfli)"}, "causes": {"ru": ["Заболевания печени", "Стоматологические заболевания", "Панкреатит", "Инфекционные процессы", "Стресс"], "en": ["Liver disease", "Dental disease", "Pancreatitis", "Infections", "Stress"], "uz": ["Jigar kasalliklari", "Tish kasalliklari", "Pankreatit", "Infeksiyalar", "Stress"]}, "emergency": True},
        {"title": {"ru": "🤮 Рвота", "en": "🤮 Vomiting", "uz": "🤮 Qusish"}, "causes": {"ru": ["Трихобезоары", "Гастрит", "Панкреатит", "Отравление", "Почечная недостаточность"], "en": ["Hairballs", "Gastritis", "Pancreatitis", "Poisoning", "Kidney failure"], "uz": ["Jun to'plari", "Gastrit", "Pankreatit", "Zaharlanish", "Buyrak yetishmovchiligi"]}, "emergency": False},
        {"title": {"ru": "🚽 Часто ходит в лоток / мало мочи", "en": "🚽 Frequent litter visits / little urine", "uz": "🚽 Tez-tez lotokka boradi / siydik kam"}, "causes": {"ru": ["Идиопатический цистит", "Мочекаменная болезнь", "Стресс"], "en": ["Idiopathic cystitis", "Urolithiasis", "Stress"], "uz": ["Idiopatik sistit", "Siydik tosh kasalligi", "Stress"]}, "emergency": False},
        {"title": {"ru": "❌ Не может помочиться", "en": "❌ Cannot urinate", "uz": "❌ Siydik chiqara olmaydi"}, "causes": {"ru": ["Обструкция уретры", "Мочекаменная болезнь"], "en": ["Urethral obstruction", "Urolithiasis"], "uz": ["Uretra obstruksiyasi", "Siydik tosh kasalligi"]}, "emergency": True},
        {"title": {"ru": "😮‍💨 Дыхание с открытым ртом", "en": "😮‍💨 Open-mouth breathing", "uz": "😮‍💨 Og'zi ochiq nafas olish"}, "causes": {"ru": ["Сердечная недостаточность", "Отёк лёгких", "Плевральный выпот", "Сильная боль"], "en": ["Heart failure", "Pulmonary edema", "Pleural effusion", "Severe pain"], "uz": ["Yurak yetishmovchiligi", "O'pka shishi", "Plevral suyuqlik", "Kuchli og'riq"]}, "emergency": True},
    ],
    "cow": [
        {"title": {"ru": "🍽️ Отказ от корма", "en": "🍽️ Feed refusal", "uz": "🍽️ Ozuqadan voz kechish"}, "causes": {"ru": ["Ацидоз рубца", "Кетоз", "Инфекции", "Послеродовые осложнения"], "en": ["Rumen acidosis", "Ketosis", "Infections", "Postpartum complications"], "uz": ["Rumen asidozi", "Ketoz", "Infeksiyalar", "Tug'ruqdan keyingi asoratlar"]}, "emergency": False},
        {"title": {"ru": "🎈 Вздутие рубца (тимпания)", "en": "🎈 Rumen bloat (tympany)", "uz": "🎈 Qorin dam bo'lishi (timponiya)"}, "causes": {"ru": ["Нарушение кормления", "Закупорка пищевода", "Пенообразующая тимпания"], "en": ["Feeding errors", "Esophageal obstruction", "Foamy bloat"], "uz": ["Oziqlantirish xatolari", "Qizilo'ngach tiqilishi", "Ko'pikli timponiya"]}, "emergency": True},
        {"title": {"ru": "🥛 Снижение удоя", "en": "🥛 Reduced milk yield", "uz": "🥛 Sut kamayishi"}, "causes": {"ru": ["Мастит", "Метаболические нарушения", "Стресс", "Хронические заболевания"], "en": ["Mastitis", "Metabolic disorders", "Stress", "Chronic diseases"], "uz": ["Mastit", "Metabolik buzilishlar", "Stress", "Surunkali kasalliklar"]}, "emergency": False},
        {"title": {"ru": "🤕 Хромота", "en": "🤕 Lameness", "uz": "🤕 Oqsoqlik"}, "causes": {"ru": ["Заболевания копыт", "Пододерматиты", "Травмы", "Дефицит микроэлементов"], "en": ["Hoof diseases", "Pododermatitis", "Injuries", "Micronutrient deficiency"], "uz": ["Tuyoq kasalliklari", "Pododermatit", "Jarohatlar", "Mikroelement yetishmovchiligi"]}, "emergency": False},
    ],
    "sheep": [
        {"title": {"ru": "💩 Диарея", "en": "💩 Diarrhea", "uz": "💩 Ich ketishi"}, "causes": {"ru": ["Кокцидиоз", "Гельминтозы", "Пищевые нарушения"], "en": ["Coccidiosis", "Helminths", "Feeding disorders"], "uz": ["Koktsidioz", "Gelmintoz", "Oziqlanish buzilishi"]}, "emergency": False},
        {"title": {"ru": "🎈 Вздутие", "en": "🎈 Bloating", "uz": "🎈 Dam bo'lish"}, "causes": {"ru": ["Тимпания", "Резкая смена корма"], "en": ["Tympany", "Sudden feed change"], "uz": ["Timponiya", "Ozuqani keskin almashtirish"]}, "emergency": False},
        {"title": {"ru": "🤕 Хромота", "en": "🤕 Lameness", "uz": "🤕 Oqsoqlik"}, "causes": {"ru": ["Гниль копыт", "Травмы", "Инфекционные процессы"], "en": ["Foot rot", "Injuries", "Infections"], "uz": ["Tuyoq chirishi", "Jarohatlar", "Infeksiyalar"]}, "emergency": False},
    ],
    "rodent": [
        {"title": {"ru": "🍽️ Не ест", "en": "🍽️ Not eating", "uz": "🍽️ Ovqat yemaydi"}, "causes": {"ru": ["Заболевания зубов", "Стресс", "Инфекции", "ЖКТ-стаз"], "en": ["Dental disease", "Stress", "Infections", "GI stasis"], "uz": ["Tish kasalliklari", "Stress", "Infeksiyalar", "OVT stazi"]}, "emergency": False},
        {"title": {"ru": "💩 Диарея", "en": "💩 Diarrhea", "uz": "💩 Ich ketishi"}, "causes": {"ru": ["Ошибки кормления", "Бактериальные инфекции", "Обезвоживание"], "en": ["Feeding errors", "Bacterial infections", "Dehydration"], "uz": ["Oziqlantirish xatolari", "Bakterial infeksiyalar", "Suvsizlanish"]}, "emergency": False},
    ],
    "bird": [
        {"title": {"ru": "🪶 Нахохленность / апатия", "en": "🪶 Fluffed up / apathy", "uz": "🪶 Patini hurpaytirish / apatiya"}, "causes": {"ru": ["Инфекции", "Переохлаждение", "Стресс"], "en": ["Infections", "Hypothermia", "Stress"], "uz": ["Infeksiyalar", "Sovqotish", "Stress"]}, "emergency": False},
        {"title": {"ru": "💩 Изменение помёта", "en": "💩 Droppings change", "uz": "💩 Najas o'zgarishi"}, "causes": {"ru": ["Заболевания ЖКТ", "Паразиты", "Печёночные заболевания"], "en": ["GI diseases", "Parasites", "Liver diseases"], "uz": ["OVT kasalliklari", "Parazitlar", "Jigar kasalliklari"]}, "emergency": False},
        {"title": {"ru": "😮‍💨 Одышка", "en": "😮‍💨 Shortness of breath", "uz": "😮‍💨 Hansirash"}, "causes": {"ru": ["Респираторные инфекции", "Аспергиллёз", "Сердечные заболевания"], "en": ["Respiratory infections", "Aspergillosis", "Heart disease"], "uz": ["Nafas yo'li infeksiyalari", "Aspergillyoz", "Yurak kasalliklari"]}, "emergency": False},
    ],
    "fish": [
        {"title": {"ru": "🐟 Лежит на дне / плавает боком", "en": "🐟 Lies at bottom / swims sideways", "uz": "🐟 Tublab yotadi / yonlab suzadi"}, "causes": {"ru": ["Нарушение параметров воды", "Поражение плавательного пузыря", "Инфекции"], "en": ["Water parameter issues", "Swim bladder disorder", "Infections"], "uz": ["Suv parametrlari buzilishi", "Suzish pufagi shikastlanishi", "Infeksiyalar"]}, "emergency": False},
        {"title": {"ru": "⚪ Белые точки", "en": "⚪ White spots", "uz": "⚪ Oq nuqtalar"}, "causes": {"ru": ["Эктопаразитарные заболевания"], "en": ["Ectoparasitic diseases"], "uz": ["Ektoparazitar kasalliklar"]}, "emergency": False},
    ],
    "exotic": [
        {"title": {"ru": "🍽️ Отказ от еды", "en": "🍽️ Food refusal", "uz": "🍽️ Ovqatdan voz kechish"}, "causes": {"ru": ["Неправильная температура", "Отсутствие УФ-B", "Стресс", "Инфекции"], "en": ["Incorrect temperature", "Lack of UV-B", "Stress", "Infections"], "uz": ["Noto'g'ri harorat", "UV-B yo'qligi", "Stress", "Infeksiyalar"]}, "emergency": False},
        {"title": {"ru": "🦴 Мягкие кости / судороги", "en": "🦴 Soft bones / seizures", "uz": "🦴 Yumshoq suyaklar / tutqanoq"}, "causes": {"ru": ["Дефицит кальция", "Метаболические болезни костей"], "en": ["Calcium deficiency", "Metabolic bone disease"], "uz": ["Kalsiy yetishmovchiligi", "Metabolik suyak kasalligi"]}, "emergency": False},
    ],
}


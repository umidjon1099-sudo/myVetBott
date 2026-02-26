from os import makedirs

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
user_city_context = {}  # Контекст раздела для выбора города (clinics/pharmacies/shelters/pet_shop)

makedirs("Главные кнопки меню", exist_ok=True)

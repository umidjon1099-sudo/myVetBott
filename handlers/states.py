"""FSM-состояния бота, используемые в обработчиках кнопок и сценариев."""
from aiogram.fsm.state import State, StatesGroup


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

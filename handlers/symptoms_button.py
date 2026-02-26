"""Кнопочный раздел проверки симптомов с поддержкой RU/EN/UZ."""
from datetime import datetime

from aiogram import F, types
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import dp
from data_store import user_languages, user_symptoms
from handlers.common import add_to_history, safe_edit_message

# ========== ТРЁХЪЯЗЫЧНАЯ БАЗА ЗНАНИЙ ПО СИМПТОМАМ ==========
SYMPTOM_KNOWLEDGE_BASE = {
    # 🐕 СОБАКИ
    "dog": {
        "вялость": {
            "ru": {
                "diseases": ["Лихорадка", "Боль", "Интоксикация", "Анемия", "Сердечная недостаточность", "Эндокринные нарушения"],
                "specialist": "Терапевт / Кардиолог / Невролог",
                "first_aid": "Обеспечьте покой, измерьте температуру. При отказе от еды или высокой температуре – срочно к врачу."
            },
            "en": {
                "diseases": ["Fever", "Pain", "Intoxication", "Anemia", "Heart failure", "Endocrine disorders"],
                "specialist": "Therapist / Cardiologist / Neurologist",
                "first_aid": "Provide rest, measure temperature. If refuses food or has high fever – see a vet immediately."
            },
            "uz": {
                "diseases": ["Isitma", "Og'riq", "Zaharlanish", "Anemiya", "Yurak yetishmovchiligi", "Endokrin buzilishlar"],
                "specialist": "Terapevt / Kardiolog / Nevrolog",
                "first_aid": "Tinchlik ta'minlang, haroratni o'lchang. Agar ovqatdan bosh tortsa yoki yuqori harorat bo'lsa – zudlik bilan veterinarga murojaat qiling."
            }
        },
        "отказ от корма": {
            "ru": {
                "diseases": ["Заболевания ЖКТ", "Заболевания печени", "Панкреатит", "Стоматологическая боль", "Инфекционные заболевания", "Стресс/боль"],
                "specialist": "Терапевт / Стоматолог",
                "first_aid": "Проверьте температуру, осмотрите ротовую полость. Если не ест более суток – к врачу."
            },
            "en": {
                "diseases": ["Gastrointestinal diseases", "Liver diseases", "Pancreatitis", "Dental pain", "Infectious diseases", "Stress/pain"],
                "specialist": "Therapist / Dentist",
                "first_aid": "Check temperature, examine oral cavity. If not eating for more than a day – see a vet."
            },
            "uz": {
                "diseases": ["Oshqozon-ichak kasalliklari", "Jigar kasalliklari", "Pankreatit", "Tish og'rig'i", "Yuqumli kasalliklar", "Stress/og'riq"],
                "specialist": "Terapevt / Stomatolog",
                "first_aid": "Haroratni tekshiring, og'iz bo'shlig'ini ko'ring. Agar bir kundan ortiq ovqat yemasangiz – veterinarga murojaat qiling."
            }
        },
        "рвота": {
            "ru": {
                "diseases": ["Гастрит/гастроэнтерит", "Инородное тело", "Отравление", "Панкреатит", "Заболевания печени", "Почечная недостаточность"],
                "specialist": "Терапевт / Гастроэнтеролог",
                "first_aid": "Не кормите 12 часов, обеспечьте водой. При повторной рвоте, крови или вялости – срочно к врачу."
            },
            "en": {
                "diseases": ["Gastritis/gastroenteritis", "Foreign body", "Poisoning", "Pancreatitis", "Liver diseases", "Kidney failure"],
                "specialist": "Therapist / Gastroenterologist",
                "first_aid": "Do not feed for 12 hours, provide water. If vomiting persists, there is blood, or lethargy – see a vet immediately."
            },
            "uz": {
                "diseases": ["Gastrit/gastroenterit", "Yot jism", "Zaharlanish", "Pankreatit", "Jigar kasalliklari", "Buyrak yetishmovchiligi"],
                "specialist": "Terapevt / Gastroenterolog",
                "first_aid": "12 soat ovqat bermang, suv bering. Agar qayt qilish takrorlansa, qon bo'lsa yoki letargiya bo'lsa – zudlik bilan veterinarga murojaat qiling."
            }
        },
        "диарея": {
            "ru": {
                "diseases": ["Паразитарные инвазии", "Бактериальные/вирусные инфекции", "Пищевая непереносимость", "Воспалительные заболевания кишечника", "Интоксикация"],
                "specialist": "Терапевт / Инфекционист",
                "first_aid": "Обеспечьте водой, легкая диета (рис, курица). При крови, рвоте или обезвоживании – к врачу."
            },
            "en": {
                "diseases": ["Parasitic infestations", "Bacterial/viral infections", "Food intolerance", "Inflammatory bowel disease", "Intoxication"],
                "specialist": "Therapist / Infectious disease specialist",
                "first_aid": "Provide water, light diet (rice, chicken). If blood, vomiting, or dehydration – see a vet."
            },
            "uz": {
                "diseases": ["Parazitar invaziyalar", "Bakterial/virusli infektsiyalar", "Oziq-ovqat intoleransi", "Ichak yallig'lanish kasalliklari", "Zaharlanish"],
                "specialist": "Terapevt / Infektsionist",
                "first_aid": "Suv bering, yengil parhez (guruch, tovuq). Agar qon, qusish yoki suvsizlanish bo'lsa – veterinarga murojaat qiling."
            }
        },
        "одышка": {
            "ru": {
                "diseases": ["Сердечная недостаточность", "Отёк лёгких", "Тепловой удар", "Плевральный выпот", "Сильная боль"],
                "specialist": "Кардиолог / Реаниматолог",
                "first_aid": "Обеспечьте покой, прохладу, доступ свежего воздуха. СРОЧНО К ВРАЧУ!"
            },
            "en": {
                "diseases": ["Heart failure", "Pulmonary edema", "Heat stroke", "Pleural effusion", "Severe pain"],
                "specialist": "Cardiologist / Emergency vet",
                "first_aid": "Provide rest, cool environment, fresh air. EMERGENCY – SEE VET IMMEDIATELY!"
            },
            "uz": {
                "diseases": ["Yurak yetishmovchiligi", "O'pka shishi", "Issiqlik urishi", "Plevral efüzyon", "Kuchli og'riq"],
                "specialist": "Kardiolog / Shoshilinch veterinar",
                "first_aid": "Tinchlik, salqinlik va toza havo ta'minlang. FAVQULODDA – ZUDLIK BILAN VETERINARGA MUROJAAT QILING!"
            }
        },
        "хромота": {
            "ru": {
                "diseases": ["Травмы", "Разрывы связок", "Артрит/остеоартроз", "Дисплазии", "Неврологические нарушения"],
                "specialist": "Хирург / Ортопед / Невролог",
                "first_aid": "Ограничьте движение, осмотрите лапу. При сильной боли или отёке – к врачу."
            },
            "en": {
                "diseases": ["Injuries", "Ligament tears", "Arthritis/osteoarthritis", "Dysplasia", "Neurological disorders"],
                "specialist": "Surgeon / Orthopedist / Neurologist",
                "first_aid": "Restrict movement, examine the paw. If severe pain or swelling – see a vet."
            },
            "uz": {
                "diseases": ["Jarohatlar", "Bog'lam yirtilishi", "Artrit/osteoartrit", "Displaziya", "Nevrologik buzilishlar"],
                "specialist": "Jarroh / Ortoped / Nevrolog",
                "first_aid": "Harakatni cheklang, panjasini tekshiring. Agar kuchli og'riq yoki shish bo'lsa – veterinarga murojaat qiling."
            }
        },
        "судороги": {
            "ru": {
                "diseases": ["Эпилепсия", "Интоксикация", "Гипогликемия", "Печёночная энцефалопатия", "Травма ЦНС"],
                "specialist": "Невролог / Реаниматолог",
                "first_aid": "Уберите предметы, о которые может удариться, не лезьте в пасть. СРОЧНО К ВРАЧУ!"
            },
            "en": {
                "diseases": ["Epilepsy", "Intoxication", "Hypoglycemia", "Hepatic encephalopathy", "CNS injury"],
                "specialist": "Neurologist / Emergency vet",
                "first_aid": "Remove objects that could cause injury, do not put hands in mouth. EMERGENCY – SEE VET IMMEDIATELY!"
            },
            "uz": {
                "diseases": ["Epilepsiya", "Zaharlanish", "Gipoglikemiya", "Jigar ensefalopatiyasi", "Markaziy asab tizimi shikastlanishi"],
                "specialist": "Nevrolog / Shoshilinch veterinar",
                "first_aid": "Urugu mumkin bo'lgan narsalarni olib tashlang, og'ziga qo'l solmang. FAVQULODDA – ZUDLIK BILAN VETERINARGA MUROJAAT QILING!"
            }
        }
    },
    # 🐱 КОШКИ
    "cat": {
        "вялость": {
            "ru": {
                "diseases": ["Вирусные инфекции", "Боль", "Заболевания почек", "Анемия", "Сердечные заболевания"],
                "specialist": "Терапевт / Нефролог",
                "first_aid": "Обеспечьте покой, измерьте температуру. При отказе от еды более суток – к врачу."
            },
            "en": {
                "diseases": ["Viral infections", "Pain", "Kidney disease", "Anemia", "Heart disease"],
                "specialist": "Therapist / Nephrologist",
                "first_aid": "Provide rest, measure temperature. If refuses food for more than a day – see a vet."
            },
            "uz": {
                "diseases": ["Virusli infektsiyalar", "Og'riq", "Buyrak kasalliklari", "Anemiya", "Yurak kasalliklari"],
                "specialist": "Terapevt / Nefrolog",
                "first_aid": "Tinchlik ta'minlang, haroratni o'lchang. Agar bir kundan ortiq ovqat yemasangiz – veterinarga murojaat qiling."
            }
        },
        "отказ от еды": {
            "ru": {
                "diseases": ["Заболевания печени", "Стоматологические заболевания", "Панкреатит", "Инфекционные процессы", "Стресс"],
                "specialist": "Терапевт / Стоматолог",
                "first_aid": "Попробуйте предложить любимый корм. При отказе более 24 часов – СРОЧНО К ВРАЧУ!"
            },
            "en": {
                "diseases": ["Liver diseases", "Dental diseases", "Pancreatitis", "Infectious processes", "Stress"],
                "specialist": "Therapist / Dentist",
                "first_aid": "Try offering favorite food. If refuses for more than 24 hours – EMERGENCY – SEE VET IMMEDIATELY!"
            },
            "uz": {
                "diseases": ["Jigar kasalliklari", "Tish kasalliklari", "Pankreatit", "Yuqumli jarayonlar", "Stress"],
                "specialist": "Terapevt / Stomatolog",
                "first_aid": "Sevimli ovqatni taklif qiling. Agar 24 soatdan ortiq ovqatlanmasa – FAVQULODDA – ZUDLIK BILAN VETERINARGA MUROJAAT QILING!"
            }
        },
        "рвота": {
            "ru": {
                "diseases": ["Трихобезоары (комки шерсти)", "Гастрит", "Панкреатит", "Отравление", "Почечная недостаточность"],
                "specialist": "Терапевт",
                "first_aid": "Дайте пасту от шерсти, не кормите 12 часов. Если рвота повторяется – к врачу."
            },
            "en": {
                "diseases": ["Trichobezoars (hairballs)", "Gastritis", "Pancreatitis", "Poisoning", "Kidney failure"],
                "specialist": "Therapist",
                "first_aid": "Give hairball paste, do not feed for 12 hours. If vomiting persists – see a vet."
            },
            "uz": {
                "diseases": ["Trikobezoarlar (jun to'plari)", "Gastrit", "Pankreatit", "Zaharlanish", "Buyrak yetishmovchiligi"],
                "specialist": "Terapevt",
                "first_aid": "Jun pastasini bering, 12 soat ovqat bermang. Agar qayt qilish takrorlansa – veterinarga murojaat qiling."
            }
        },
        "часто ходит в лоток": {
            "ru": {
                "diseases": ["Идиопатический цистит", "Мочекаменная болезнь", "Стресс"],
                "specialist": "Уролог / Нефролог",
                "first_aid": "Обеспечьте доступ к воде, уберите стресс. При крови или затруднённом мочеиспускании – СРОЧНО К ВРАЧУ!"
            },
            "en": {
                "diseases": ["Idiopathic cystitis", "Urinary stones", "Stress"],
                "specialist": "Urologist / Nephrologist",
                "first_aid": "Provide access to water, reduce stress. If blood or difficulty urinating – EMERGENCY – SEE VET IMMEDIATELY!"
            },
            "uz": {
                "diseases": ["Idiopatik sistit", "Siydik-tosh kasalligi", "Stress"],
                "specialist": "Urolog / Nefrolog",
                "first_aid": "Suvga kirishni ta'minlang, stressni kamaytiring. Agar qon yoki siyish qiyin bo'lsa – FAVQULODDA – ZUDLIK BILAN VETERINARGA MUROJAAT QILING!"
            }
        },
        "не может помочиться": {
            "ru": {
                "diseases": ["Обструкция уретры", "Мочекаменная болезнь"],
                "specialist": "Хирург / Уролог",
                "first_aid": "СРОЧНО К ВРАЧУ! Это жизнеугрожающее состояние."
            },
            "en": {
                "diseases": ["Urethral obstruction", "Urinary stones"],
                "specialist": "Surgeon / Urologist",
                "first_aid": "EMERGENCY – SEE VET IMMEDIATELY! This is life-threatening."
            },
            "uz": {
                "diseases": ["Uretra obstruktsiyasi", "Siydik-tosh kasalligi"],
                "specialist": "Jarroh / Urolog",
                "first_aid": "FAVQULODDA – ZUDLIK BILAN VETERINARGA MUROJAAT QILING! Bu hayot uchun xavfli holat."
            }
        },
        "одышка": {
            "ru": {
                "diseases": ["Сердечная недостаточность", "Отёк лёгких", "Плевральный выпот", "Сильная боль"],
                "specialist": "Кардиолог / Реаниматолог",
                "first_aid": "СРОЧНО К ВРАЧУ! Обеспечьте покой, не беспокойте."
            },
            "en": {
                "diseases": ["Heart failure", "Pulmonary edema", "Pleural effusion", "Severe pain"],
                "specialist": "Cardiologist / Emergency vet",
                "first_aid": "EMERGENCY – SEE VET IMMEDIATELY! Provide rest, do not disturb."
            },
            "uz": {
                "diseases": ["Yurak yetishmovchiligi", "O'pka shishi", "Plevral efüzyon", "Kuchli og'riq"],
                "specialist": "Kardiolog / Shoshilinch veterinar",
                "first_aid": "FAVQULODDA – ZUDLIK BILAN VETERINARGA MUROJAAT QILING! Tinchlik ta'minlang, bezovta qilmang."
            }
        }
    },
    # 🐄 КОРОВЫ (КРС)
    "cow": {
        "отказ от корма": {
            "ru": {
                "diseases": ["Ацидоз рубца", "Кетоз", "Инфекционные заболевания", "Послеродовые осложнения"],
                "specialist": "Ветеринарный врач (терапевт)",
                "first_aid": "Проверьте температуру, вызовите ветеринара."
            },
            "en": {
                "diseases": ["Rumen acidosis", "Ketosis", "Infectious diseases", "Postpartum complications"],
                "specialist": "Veterinarian (therapist)",
                "first_aid": "Check temperature, call a vet."
            },
            "uz": {
                "diseases": ["Kislotali rumen", "Ketoz", "Yuqumli kasalliklar", "Tug'ruqdan keyingi asoratlar"],
                "specialist": "Veterinar (terapevt)",
                "first_aid": "Haroratni tekshiring, veterinarni chaqiring."
            }
        },
        "вздутие": {
            "ru": {
                "diseases": ["Тимпания", "Нарушение кормления", "Закупорка пищевода"],
                "specialist": "Ветеринарный врач (хирург/терапевт)",
                "first_aid": "СРОЧНО вызовите ветеринара! При острой тимпании требуется прокол рубца."
            },
            "en": {
                "diseases": ["Tympany", "Feeding disorders", "Esophageal obstruction"],
                "specialist": "Veterinarian (surgeon/therapist)",
                "first_aid": "EMERGENCY – call a vet immediately! Acute tympany requires rumen puncture."
            },
            "uz": {
                "diseases": ["Timpaniya", "Oziqlantirish buzilishlari", "Qizilo'ngach obstruktsiyasi"],
                "specialist": "Veterinar (jarroh/terapevt)",
                "first_aid": "FAVQULODDA – zudlik bilan veterinarni chaqiring! O'tkir timpaniyada rumen teshilishi kerak."
            }
        },
        "снижение удоя": {
            "ru": {
                "diseases": ["Мастит", "Метаболические нарушения", "Стресс", "Хронические заболевания"],
                "specialist": "Ветеринарный врач",
                "first_aid": "Проверьте вымя, осмотрите корову, вызовите специалиста."
            },
            "en": {
                "diseases": ["Mastitis", "Metabolic disorders", "Stress", "Chronic diseases"],
                "specialist": "Veterinarian",
                "first_aid": "Check the udder, examine the cow, call a specialist."
            },
            "uz": {
                "diseases": ["Mastit", "Metabolik buzilishlar", "Stress", "Surunkali kasalliklar"],
                "specialist": "Veterinar",
                "first_aid": "Elinini tekshiring, sigirni ko'ring, mutaxassisni chaqiring."
            }
        },
        "хромота": {
            "ru": {
                "diseases": ["Заболевания копыт", "Пододерматиты", "Травмы", "Дефицит микроэлементов"],
                "specialist": "Ортопед / Хирург",
                "first_aid": "Осмотрите копыта, обеспечьте мягкую подстилку, вызовите ветеринара."
            },
            "en": {
                "diseases": ["Hoof diseases", "Pododermatitis", "Injuries", "Micronutrient deficiency"],
                "specialist": "Orthopedist / Surgeon",
                "first_aid": "Examine hooves, provide soft bedding, call a vet."
            },
            "uz": {
                "diseases": ["Tuyoq kasalliklari", "Pododermatit", "Jarohatlar", "Mikroelementlar etishmasligi"],
                "specialist": "Ortoped / Jarroh",
                "first_aid": "Tuyoqlarni tekshiring, yumshoq to'shak ta'minlang, veterinarni chaqiring."
            }
        }
    },
    # 🐏 ОВЦЫ / БАРАНЫ
    "sheep": {
        "диарея": {
            "ru": {
                "diseases": ["Кокцидиоз", "Гельминтозы", "Пищевые нарушения"],
                "specialist": "Ветеринарный врач (паразитолог)",
                "first_aid": "Обеспечьте водой. При сильной диарее – вызовите врача."
            },
            "en": {
                "diseases": ["Coccidiosis", "Helminthiasis", "Nutritional disorders"],
                "specialist": "Veterinarian (parasitologist)",
                "first_aid": "Provide water. If severe diarrhea – call a vet."
            },
            "uz": {
                "diseases": ["Koksidioz", "Gelmintoz", "Oziqlantirish buzilishlari"],
                "specialist": "Veterinar (parazitolog)",
                "first_aid": "Suv bering. Agar kuchli diareya bo'lsa – veterinarni chaqiring."
            }
        },
        "вздутие": {
            "ru": {
                "diseases": ["Тимпания", "Резкая смена корма"],
                "specialist": "Ветеринарный врач",
                "first_aid": "СРОЧНО вызовите врача!"
            },
            "en": {
                "diseases": ["Tympany", "Sudden feed change"],
                "specialist": "Veterinarian",
                "first_aid": "EMERGENCY – call a vet immediately!"
            },
            "uz": {
                "diseases": ["Timpaniya", "To'satdan ozuqa o'zgarishi"],
                "specialist": "Veterinar",
                "first_aid": "FAVQULODDA – zudlik bilan veterinarni chaqiring!"
            }
        },
        "хромота": {
            "ru": {
                "diseases": ["Гниль копыт", "Травмы", "Инфекционные процессы"],
                "specialist": "Хирург / Ортопед",
                "first_aid": "Осмотрите копыта, обработайте антисептиком, вызовите врача."
            },
            "en": {
                "diseases": ["Foot rot", "Injuries", "Infectious processes"],
                "specialist": "Surgeon / Orthopedist",
                "first_aid": "Examine hooves, treat with antiseptic, call a vet."
            },
            "uz": {
                "diseases": ["Tuyoq chirishi", "Jarohatlar", "Yuqumli jarayonlar"],
                "specialist": "Jarroh / Ortoped",
                "first_aid": "Tuyoqlarni tekshiring, antiseptik bilan ishlang, veterinarni chaqiring."
            }
        }
    },
    # 🐹 ГРЫЗУНЫ
    "rodent": {
        "не ест": {
            "ru": {
                "diseases": ["Заболевания зубов", "Стресс", "Инфекционные заболевания", "ЖКТ-стаз"],
                "specialist": "Ратолог / Ветеринар для грызунов",
                "first_aid": "Проверьте зубы, обеспечьте тепло. При отказе от еды более 12 часов – срочно к врачу."
            },
            "en": {
                "diseases": ["Dental diseases", "Stress", "Infectious diseases", "GI stasis"],
                "specialist": "Rodent veterinarian",
                "first_aid": "Check teeth, provide warmth. If refuses food for more than 12 hours – see a vet immediately."
            },
            "uz": {
                "diseases": ["Tish kasalliklari", "Stress", "Yuqumli kasalliklar", "Oshqozon-ichak stazi"],
                "specialist": "Kemiruvchilar veterinari",
                "first_aid": "Tishlarni tekshiring, issiqlik ta'minlang. Agar 12 soatdan ortiq ovqat yemasangiz – zudlik bilan veterinarga murojaat qiling."
            }
        },
        "диарея": {
            "ru": {
                "diseases": ["Ошибки кормления", "Бактериальные инфекции", "Обезвоживание"],
                "specialist": "Ратолог",
                "first_aid": "Уберите сочные корма, обеспечьте водой. При ухудшении – к врачу."
            },
            "en": {
                "diseases": ["Feeding errors", "Bacterial infections", "Dehydration"],
                "specialist": "Rodent veterinarian",
                "first_aid": "Remove juicy foods, provide water. If worsens – see a vet."
            },
            "uz": {
                "diseases": ["Oziqlantirish xatolari", "Bakterial infektsiyalar", "Suvsizlanish"],
                "specialist": "Kemiruvchilar veterinari",
                "first_aid": "Sersuv ovqatlarni olib tashlang, suv bering. Agar yomonlashsa – veterinarga murojaat qiling."
            }
        }
    },
    # 🐦 ПТИЦЫ
    "bird": {
        "нахохленность": {
            "ru": {
                "diseases": ["Инфекционные заболевания", "Переохлаждение", "Стресс"],
                "specialist": "Орнитолог",
                "first_aid": "Обеспечьте тепло, покой. При отказе от корма – к врачу."
            },
            "en": {
                "diseases": ["Infectious diseases", "Hypothermia", "Stress"],
                "specialist": "Avian vet",
                "first_aid": "Provide warmth, rest. If refuses food – see a vet."
            },
            "uz": {
                "diseases": ["Yuqumli kasalliklar", "Sovuq urishi", "Stress"],
                "specialist": "Ornitolog",
                "first_aid": "Issiqlik va tinchlik ta'minlang. Agar ovqatdan bosh tortsa – veterinarga murojaat qiling."
            }
        },
        "изменение помёта": {
            "ru": {
                "diseases": ["Заболевания ЖКТ", "Паразиты", "Печёночные заболевания"],
                "specialist": "Орнитолог",
                "first_aid": "Проверьте корм, обеспечьте чистой водой. При ухудшении – к врачу."
            },
            "en": {
                "diseases": ["Gastrointestinal diseases", "Parasites", "Liver diseases"],
                "specialist": "Avian vet",
                "first_aid": "Check food, provide clean water. If worsens – see a vet."
            },
            "uz": {
                "diseases": ["Oshqozon-ichak kasalliklari", "Parazitlar", "Jigar kasalliklari"],
                "specialist": "Ornitolog",
                "first_aid": "Ozuqani tekshiring, toza suv bering. Agar yomonlashsa – veterinarga murojaat qiling."
            }
        },
        "одышка": {
            "ru": {
                "diseases": ["Респираторные инфекции", "Аспергиллёз", "Сердечные заболевания"],
                "specialist": "Орнитолог",
                "first_aid": "Обеспечьте покой, тепло. СРОЧНО К ВРАЧУ!"
            },
            "en": {
                "diseases": ["Respiratory infections", "Aspergillosis", "Heart diseases"],
                "specialist": "Avian vet",
                "first_aid": "Provide rest, warmth. EMERGENCY – SEE VET IMMEDIATELY!"
            },
            "uz": {
                "diseases": ["Nafas olish infektsiyalari", "Aspergillyoz", "Yurak kasalliklari"],
                "specialist": "Ornitolog",
                "first_aid": "Tinchlik va issiqlik ta'minlang. FAVQULODDA – ZUDLIK BILAN VETERINARGA MUROJAAT QILING!"
            }
        }
    },
    # 🐠 РЫБКИ
    "fish": {
        "лежит на дне": {
            "ru": {
                "diseases": ["Нарушение параметров воды", "Поражение плавательного пузыря", "Инфекционные заболевания"],
                "specialist": "Ихтиопатолог",
                "first_aid": "Проверьте воду (аммиак, нитриты), подмените воду. При ухудшении – обратитесь к специалисту."
            },
            "en": {
                "diseases": ["Water parameter imbalance", "Swim bladder disorder", "Infectious diseases"],
                "specialist": "Fish vet (ichthyopathologist)",
                "first_aid": "Check water (ammonia, nitrites), change water. If worsens – consult a specialist."
            },
            "uz": {
                "diseases": ["Suv parametrlarining buzilishi", "Suzish pufagi kasalligi", "Yuqumli kasalliklar"],
                "specialist": "Ixtiopatolog",
                "first_aid": "Suvni tekshiring (ammiak, nitritlar), suvni almashtiring. Agar yomonlashsa – mutaxassisga murojaat qiling."
            }
        },
        "белые точки": {
            "ru": {
                "diseases": ["Эктопаразитарные заболевания (ихтиофтириус)"],
                "specialist": "Ихтиопатолог",
                "first_aid": "Повысьте температуру, добавьте специальные препараты, карантин."
            },
            "en": {
                "diseases": ["Ectoparasitic diseases (ichthyophthirius)"],
                "specialist": "Fish vet (ichthyopathologist)",
                "first_aid": "Raise temperature, add special medications, quarantine."
            },
            "uz": {
                "diseases": ["Ektoparazitar kasalliklar (ichthyophthirius)"],
                "specialist": "Ixtiopatolog",
                "first_aid": "Haroratni ko'taring, maxsus preparatlar qo'shing, karantin."
            }
        }
    },
    # 🦎 ЭКЗОТИЧЕСКИЕ (рептилии)
    "exotic": {
        "отказ от еды": {
            "ru": {
                "diseases": ["Неправильная температура", "Отсутствие УФ-В", "Стресс", "Инфекционные заболевания"],
                "specialist": "Герпетолог",
                "first_aid": "Проверьте температуру и освещение в террариуме. При отказе более 2 недель – к врачу."
            },
            "en": {
                "diseases": ["Improper temperature", "Lack of UV-B", "Stress", "Infectious diseases"],
                "specialist": "Herpetologist",
                "first_aid": "Check temperature and lighting in the terrarium. If refuses for more than 2 weeks – see a vet."
            },
            "uz": {
                "diseases": ["Noto'g'ri harorat", "UV-B yetishmasligi", "Stress", "Yuqumli kasalliklar"],
                "specialist": "Gerpetolog",
                "first_aid": "Terrariumdagi harorat va yoritishni tekshiring. Agar 2 haftadan ortiq ovqatlanmasa – veterinarga murojaat qiling."
            }
        },
        "мягкие кости": {
            "ru": {
                "diseases": ["Дефицит кальция", "Метаболические болезни костей"],
                "specialist": "Герпетолог",
                "first_aid": "Добавьте кальций и УФ-лампу. СРОЧНО К ВРАЧУ!"
            },
            "en": {
                "diseases": ["Calcium deficiency", "Metabolic bone disease"],
                "specialist": "Herpetologist",
                "first_aid": "Add calcium and UV-B lamp. EMERGENCY – SEE VET IMMEDIATELY!"
            },
            "uz": {
                "diseases": ["Kaltsiy etishmasligi", "Metabolik suyak kasalligi"],
                "specialist": "Gerpetolog",
                "first_aid": "Kaltsiy va UV-B chiroq qo'shing. FAVQULODDA – ZUDLIK BILAN VETERINARGA MUROJAAT QILING!"
            }
        }
    }
}


ANIMAL_LABELS = {
    "dog": {"ru": "🐕 Собаки", "en": "🐕 Dogs", "uz": "🐕 Itlar"},
    "cat": {"ru": "🐱 Кошки", "en": "🐱 Cats", "uz": "🐱 Mushuklar"},
    "cow": {"ru": "🐄 Коровы", "en": "🐄 Cows", "uz": "🐄 Sigirlar"},
    "sheep": {"ru": "🐏 Бараны / Овцы", "en": "🐏 Rams / Sheep", "uz": "🐏 Qo'y / Qo'chqor"},
    "rodent": {"ru": "🐹 Грызуны", "en": "🐹 Rodents", "uz": "🐹 Kemiruvchilar"},
    "bird": {"ru": "🐦 Птицы", "en": "🐦 Birds", "uz": "🐦 Qushlar"},
    "fish": {"ru": "🐠 Рыбки", "en": "🐠 Fish", "uz": "🐠 Baliqlar"},
    "exotic": {"ru": "🦎 Экзотические", "en": "🦎 Exotic Pets", "uz": "🦎 Ekzotiklar"},
}

SYMPTOM_LABELS = {
    "вялость": {"ru": "😴 Вялость / слабость", "en": "😴 Lethargy / weakness", "uz": "😴 Loqaydlik / holsizlik"},
    "отказ от корма": {"ru": "🍽️ Отказ от корма / анорексия", "en": "🍽️ Food refusal / anorexia", "uz": "🍽️ Ozuqadan voz kechish"},
    "рвота": {"ru": "🤮 Рвота", "en": "🤮 Vomiting", "uz": "🤮 Qusish"},
    "диарея": {"ru": "💩 Диарея", "en": "💩 Diarrhea", "uz": "💩 Ich ketishi"},
    "одышка": {"ru": "😮‍💨 Одышка / учащённое дыхание", "en": "😮‍💨 Shortness of breath", "uz": "😮‍💨 Hansirash"},
    "хромота": {"ru": "🤕 Хромота", "en": "🤕 Lameness", "uz": "🤕 Oqsoqlik"},
    "судороги": {"ru": "⚡ Судороги", "en": "⚡ Seizures", "uz": "⚡ Tutqanoq"},
    "отказ от еды": {"ru": "🍽️ Отказ от еды", "en": "🍽️ Food refusal", "uz": "🍽️ Ovqat yemaydi"},
    "часто ходит в лоток": {"ru": "🚽 Часто ходит в лоток / мало мочи", "en": "🚽 Frequent litter visits / little urine", "uz": "🚽 Tez-tez lotok / kam siydik"},
    "не может помочиться": {"ru": "❌ Не может помочиться", "en": "❌ Cannot urinate", "uz": "❌ Siydik chiqara olmaydi"},
    "вздутие": {"ru": "🎈 Вздутие", "en": "🎈 Bloating", "uz": "🎈 Dam bo'lish"},
    "не ест": {"ru": "🍽️ Не ест", "en": "🍽️ Not eating", "uz": "🍽️ Ovqat yemaydi"},
    "нахохленность": {"ru": "🪶 Нахохленность / апатия", "en": "🪶 Fluffed up / apathy", "uz": "🪶 Hurpaygan / apatiya"},
    "изменение помёта": {"ru": "💩 Изменение помёта", "en": "💩 Droppings change", "uz": "💩 Najas o'zgarishi"},
    "лежит на дне": {"ru": "🐟 Лежит на дне / плавает боком", "en": "🐟 Bottom sitting / sideways swimming", "uz": "🐟 Tublab yotadi / yonlab suzadi"},
    "белые точки": {"ru": "⚪ Белые точки", "en": "⚪ White spots", "uz": "⚪ Oq nuqtalar"},
    "мягкие кости": {"ru": "🦴 Мягкие кости / судороги", "en": "🦴 Soft bones / seizures", "uz": "🦴 Yumshoq suyaklar / tutqanoq"},
}

LOCAL_UI = {
    "choose_animal": {
        "ru": "🩺 <b>Проверка симптомов</b>\n\nВыберите животное:",
        "en": "🩺 <b>Symptom Checker</b>\n\nChoose animal:",
        "uz": "🩺 <b>Simptomlarni tekshirish</b>\n\nHayvonni tanlang:",
    },
    "choose_symptom": {
        "ru": "Выберите симптом:",
        "en": "Choose a symptom:",
        "uz": "Simptomni tanlang:",
    },
    "possible_diseases": {
        "ru": "Возможные причины",
        "en": "Possible causes",
        "uz": "Ehtimoliy sabablar",
    },
    "specialist": {
        "ru": "Рекомендуемый специалист",
        "en": "Recommended specialist",
        "uz": "Tavsiya etilgan mutaxassis",
    },
    "first_aid": {
        "ru": "Первая помощь",
        "en": "First aid",
        "uz": "Birinchi yordam",
    },
    "back_animals": {
        "ru": "🔙 К выбору животного",
        "en": "🔙 Back to animal choice",
        "uz": "🔙 Hayvon tanlashga qaytish",
    },
    "back_symptoms": {
        "ru": "🔙 К симптомам",
        "en": "🔙 Back to symptoms",
        "uz": "🔙 Simptomlarga qaytish",
    },
    "main_menu": {
        "ru": "🏠 Главное меню",
        "en": "🏠 Main Menu",
        "uz": "🏠 Asosiy menyu",
    },
}


def _lang(user_id: int) -> str:
    return user_languages.get(user_id, "ru")


def _tr(user_id: int, key: str) -> str:
    lang = _lang(user_id)
    return LOCAL_UI[key].get(lang, LOCAL_UI[key]["ru"])


def _animal_text(user_id: int, animal_id: str) -> str:
    lang = _lang(user_id)
    return ANIMAL_LABELS[animal_id].get(lang, ANIMAL_LABELS[animal_id]["ru"])


def _symptom_text(user_id: int, symptom_key: str) -> str:
    lang = _lang(user_id)
    label = SYMPTOM_LABELS.get(symptom_key)
    if not label:
        return symptom_key
    return label.get(lang, label["ru"])


def _animals_keyboard(user_id: int) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=_animal_text(user_id, animal_id), callback_data=f"sym_animal_{animal_id}")] for animal_id in ANIMAL_LABELS]
    rows.append([InlineKeyboardButton(text=_tr(user_id, "main_menu"), callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _symptoms_keyboard(user_id: int, animal_id: str) -> InlineKeyboardMarkup:
    symptom_keys = list(SYMPTOM_KNOWLEDGE_BASE.get(animal_id, {}).keys())
    rows = [
        [InlineKeyboardButton(text=_symptom_text(user_id, symptom_key), callback_data=f"symptom_{animal_id}_{idx}")]
        for idx, symptom_key in enumerate(symptom_keys)
    ]
    rows.append([InlineKeyboardButton(text=_tr(user_id, "back_animals"), callback_data="menu_symptoms")])
    rows.append([InlineKeyboardButton(text=_tr(user_id, "main_menu"), callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


@dp.callback_query(F.data == "menu_symptoms")
async def symptoms_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await safe_edit_message(
        callback.message,
        _tr(user_id, "choose_animal"),
        reply_markup=_animals_keyboard(user_id),
        parse_mode=ParseMode.HTML,
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("sym_animal_"))
async def choose_animal(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    animal_id = callback.data.replace("sym_animal_", "")

    if animal_id not in SYMPTOM_KNOWLEDGE_BASE:
        await callback.answer("Unknown animal")
        return

    await safe_edit_message(
        callback.message,
        f"{_animal_text(user_id, animal_id)}\n\n{_tr(user_id, 'choose_symptom')}",
        reply_markup=_symptoms_keyboard(user_id, animal_id),
        parse_mode=ParseMode.HTML,
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("symptom_"))
async def show_symptom_details(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    payload = callback.data.replace("symptom_", "")

    try:
        animal_id, idx_raw = payload.rsplit("_", 1)
        idx = int(idx_raw)
    except (ValueError, TypeError):
        await callback.answer("Invalid symptom")
        return

    symptom_keys = list(SYMPTOM_KNOWLEDGE_BASE.get(animal_id, {}).keys())
    if idx < 0 or idx >= len(symptom_keys):
        await callback.answer("Invalid symptom")
        return

    symptom_key = symptom_keys[idx]
    lang = _lang(user_id)
    symptom_data = SYMPTOM_KNOWLEDGE_BASE[animal_id][symptom_key][lang]
    symptom_title = _symptom_text(user_id, symptom_key)

    user_symptoms.setdefault(user_id, []).append(
        {
            "animal": animal_id,
            "symptom": symptom_title,
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
    )
    add_to_history(user_id, f"🩺 Симптом: {symptom_title}")

    text = (
        f"{_animal_text(user_id, animal_id)}\n\n"
        f"<b>{symptom_title}</b>\n\n"
        f"<b>{_tr(user_id, 'possible_diseases')}:</b>\n"
        + "\n".join(f"• {d}" for d in symptom_data["diseases"])
        + f"\n\n<b>{_tr(user_id, 'specialist')}:</b>\n• {symptom_data['specialist']}"
        + f"\n\n<b>{_tr(user_id, 'first_aid')}:</b>\n{symptom_data['first_aid']}"
    )

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=_tr(user_id, "back_symptoms"), callback_data=f"sym_animal_{animal_id}")],
                [InlineKeyboardButton(text=_tr(user_id, "back_animals"), callback_data="menu_symptoms")],
                [InlineKeyboardButton(text=_tr(user_id, "main_menu"), callback_data="back_to_menu")],
            ]
        ),
        parse_mode=ParseMode.HTML,
    )
    await callback.answer()

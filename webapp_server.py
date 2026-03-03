import hashlib
import hmac
import json
import os
import random
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qsl

from aiohttp import web

from bot_data import (
    ANIMAL_FACTS,
    CLINICS_DATA,
    FEEDING_INFO,
    PHARMACIES_DATA,
    SHELTERS_DATA,
    SYMPTOM_ANIMALS,
    SYMPTOM_LIBRARY,
    TEXTS,
    UZBEK_CITIES,
)
from data_store import (
    user_ads,
    user_history,
    user_languages,
    user_profiles,
    user_reminders,
    user_symptoms,
    vet_profiles,
)
from handlers.common import add_to_history
from handlers.vet_chat_button import DIRECTIONS

BASE_DIR = Path(__file__).resolve().parent
WEBAPP_DIR = BASE_DIR / "webapp"

NEWS_ITEMS = {
    "ru": [
        "В Ташкенте открылся новый приют для бездомных животных",
        "Бесплатная вакцинация собак от бешенства в Самарканде",
        "Конкурс на лучший зоомагазин Узбекистана 2024",
        "Новый закон о защите животных в Узбекистане",
    ],
    "en": [
        "A new shelter for stray animals opened in Tashkent",
        "Free rabies vaccination for dogs in Samarkand",
        "Contest for the best pet shop in Uzbekistan 2024",
        "New animal protection law in Uzbekistan",
    ],
    "uz": [
        "Toshkentda qarovsiz hayvonlar uchun yangi boshpana ochildi",
        "Samarqandda itlarga quturishga qarshi bepul emlash",
        "O'zbekistondagi eng yaxshi zo'odokon tanlovi 2024",
        "O'zbekistonda hayvonlarni himoya qilish bo'yicha yangi qonun",
    ],
}


class AuthError(Exception):
    pass


def _json_error(message: str, status: int = 400) -> web.Response:
    return web.json_response({"ok": False, "error": message}, status=status)


def _text(lang: str, key: str) -> str:
    return TEXTS.get(key, {}).get(lang, TEXTS.get(key, {}).get("ru", key))


def _get_lang(user_id: int) -> str:
    return user_languages.get(user_id, "ru")


def _validate_init_data(init_data: str, bot_token: str) -> dict:
    if not init_data:
        raise AuthError("Missing Telegram init data")

    pairs = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = pairs.pop("hash", None)
    if not received_hash:
        raise AuthError("Invalid Telegram init data hash")

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(pairs.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise AuthError("Telegram init data verification failed")

    auth_date = pairs.get("auth_date")
    if auth_date:
        try:
            auth_ts = int(auth_date)
            if abs(int(time.time()) - auth_ts) > 60 * 60 * 24 * 7:
                raise AuthError("Telegram auth data expired")
        except ValueError as exc:
            raise AuthError("Invalid auth_date") from exc

    user_raw = pairs.get("user")
    if not user_raw:
        raise AuthError("Missing Telegram user")

    try:
        user = json.loads(user_raw)
    except json.JSONDecodeError as exc:
        raise AuthError("Invalid Telegram user payload") from exc

    return user


def _get_user(request: web.Request) -> dict:
    bot_token = request.app["bot_token"]
    init_data = request.headers.get("X-Telegram-Init-Data", "")

    if not init_data:
        dev_user_id = os.getenv("WEBAPP_DEV_USER_ID")
        if dev_user_id:
            return {"id": int(dev_user_id), "first_name": "Dev"}

    return _validate_init_data(init_data, bot_token)


def _require_user(request: web.Request) -> dict:
    try:
        user = _get_user(request)
    except AuthError as exc:
        raise web.HTTPUnauthorized(text=str(exc)) from exc

    user_id = int(user["id"])
    user_languages.setdefault(user_id, "ru")
    user_profiles.setdefault(user_id, {})
    user_symptoms.setdefault(user_id, [])
    user_reminders.setdefault(user_id, [])
    user_history.setdefault(user_id, [])
    user_ads.setdefault(user_id, [])
    return user


def _cities_payload(lang: str) -> list:
    return [{"key": key, "name": _text(lang, key)} for key in UZBEK_CITIES]


def _direction_name(lang: str, idx: int) -> str:
    data = DIRECTIONS[idx]
    return data.get(lang, data["ru"])


def _direction_aliases(idx: int) -> list:
    data = DIRECTIONS[idx]
    return [v.lower() for v in data.values()]


async def index_page(_: web.Request) -> web.Response:
    return web.FileResponse(WEBAPP_DIR / "index.html")


async def static_file(request: web.Request) -> web.Response:
    name = request.match_info["name"]
    allowed = {"app.js", "styles.css"}
    if name not in allowed:
        raise web.HTTPNotFound()
    return web.FileResponse(WEBAPP_DIR / name)


async def api_bootstrap(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    lang = _get_lang(user_id)
    full_name = " ".join(part for part in [user.get("first_name"), user.get("last_name")] if part).strip()

    payload = {
        "ok": True,
        "user": {"id": user_id, "name": full_name or user.get("username") or f"User {user_id}"},
        "lang": lang,
        "cities": _cities_payload(lang),
        "has_pet_profile": bool(user_profiles.get(user_id)),
        "has_vet_profile": bool(vet_profiles.get(user_id)),
        "features": {
            "appointment_online": False,
            "feeding_farm_ready": False,
            "feeding_exotic_ready": False,
            "geolocation_ready": False,
        },
    }
    return web.json_response(payload)


async def api_set_language(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    body = await request.json()
    lang = body.get("lang", "ru")
    if lang not in {"ru", "en", "uz"}:
        return _json_error("Unsupported language")

    user_languages[user_id] = lang
    add_to_history(user_id, f"🌍 Language changed: {lang}")
    return web.json_response({"ok": True, "lang": lang})


async def api_get_profiles(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    return web.json_response(
        {
            "ok": True,
            "pet_profile": user_profiles.get(user_id, {}),
            "vet_profile": vet_profiles.get(user_id, {}),
        }
    )


async def api_save_pet_profile(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    body = await request.json()

    profile_data = {
        "owner_name": body.get("owner_name", "").strip(),
        "owner_phone": body.get("owner_phone", "").strip(),
        "city": body.get("city", "").strip(),
        "pet_name": body.get("pet_name", "").strip(),
        "pet_type": body.get("pet_type", "").strip(),
        "pet_breed": body.get("pet_breed", "").strip(),
        "pet_age": body.get("pet_age", "").strip(),
        "pet_weight": body.get("pet_weight", "").strip(),
        "pet_color": body.get("pet_color", "").strip(),
        "allergies": body.get("allergies", "").strip(),
        "diseases": body.get("diseases", "").strip(),
        "vaccinations": body.get("vaccinations", "").strip(),
        "pet_photo": body.get("pet_photo", "").strip(),
    }

    if not profile_data["owner_name"] or not profile_data["pet_name"]:
        return _json_error("Owner name and pet name are required")

    user_profiles[user_id] = profile_data
    add_to_history(user_id, f"👤 Saved pet profile: {profile_data['pet_name']}")
    return web.json_response({"ok": True, "profile": profile_data})


async def api_save_vet_profile(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    body = await request.json()

    profile_data = {
        "vet_name": body.get("vet_name", "").strip(),
        "vet_phone": body.get("vet_phone", "").strip(),
        "vet_city": body.get("vet_city", "").strip(),
        "vet_specialization": body.get("vet_specialization", "").strip(),
        "vet_experience": body.get("vet_experience", "").strip(),
        "vet_education": body.get("vet_education", "").strip(),
        "vet_telegram": body.get("vet_telegram", "").strip(),
        "vet_consultation_price": body.get("vet_consultation_price", "").strip(),
        "vet_info": body.get("vet_info", "").strip(),
        "vet_photo": body.get("vet_photo", "").strip(),
    }

    if not profile_data["vet_name"]:
        return _json_error("Vet name is required")

    vet_profiles[user_id] = profile_data
    add_to_history(user_id, "👨‍⚕️ Saved vet profile")
    return web.json_response({"ok": True, "profile": profile_data})


async def api_directory(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    lang = _get_lang(user_id)

    section = request.match_info["section"]
    city = request.match_info["city"]

    source = {
        "clinics": CLINICS_DATA,
        "pharmacies": PHARMACIES_DATA,
        "shelters": SHELTERS_DATA,
        "pet_shop": PHARMACIES_DATA,
    }.get(section)
    if source is None:
        return _json_error("Unsupported section")

    items = source.get(city, [])
    city_name = _text(lang, city)
    map_link = f"https://www.google.com/maps/search/veterinary+{section}+{city_name}"
    return web.json_response({"ok": True, "items": items, "map_link": map_link})


async def api_news(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    lang = _get_lang(user_id)
    return web.json_response({"ok": True, "items": NEWS_ITEMS.get(lang, NEWS_ITEMS["ru"])})


async def api_random_fact(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    lang = _get_lang(user_id)
    fact = random.choice(ANIMAL_FACTS.get(lang, ANIMAL_FACTS["ru"]))
    return web.json_response({"ok": True, "fact": fact})


async def api_feeding(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    lang = _get_lang(user_id)
    animal = request.match_info["animal"]

    text = FEEDING_INFO.get(animal, {}).get(lang)
    if not text:
        text = {
            "ru": "Информация обновляется...",
            "en": "Information is being updated...",
            "uz": "Ma'lumot yangilanmoqda...",
        }.get(lang, "Information is being updated...")

    return web.json_response({"ok": True, "text": text})


async def api_symptom_animals(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    lang = _get_lang(user_id)

    items = []
    for animal_id, data in SYMPTOM_ANIMALS.items():
        items.append(
            {
                "id": animal_id,
                "label": f"{data['emoji']} {data['name'].get(lang, data['name']['ru'])}",
            }
        )
    return web.json_response({"ok": True, "items": items})


async def api_symptom_list(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    lang = _get_lang(user_id)
    animal = request.match_info["animal"]

    if animal not in SYMPTOM_LIBRARY:
        return _json_error("Unknown animal")

    items = []
    for idx, row in enumerate(SYMPTOM_LIBRARY[animal]):
        items.append({"idx": idx, "title": row["title"].get(lang, row["title"]["ru"])})

    return web.json_response({"ok": True, "items": items})


async def api_symptom_details(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    lang = _get_lang(user_id)
    animal = request.match_info["animal"]

    try:
        idx = int(request.match_info["idx"])
    except ValueError:
        return _json_error("Invalid symptom index")

    rows = SYMPTOM_LIBRARY.get(animal, [])
    if idx < 0 or idx >= len(rows):
        return _json_error("Invalid symptom index")

    row = rows[idx]
    title = row["title"].get(lang, row["title"]["ru"])
    causes = row["causes"].get(lang, row["causes"]["ru"])

    user_symptoms.setdefault(user_id, []).append(
        {
            "animal": animal,
            "symptom": title,
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
    )
    add_to_history(user_id, f"🩺 Symptom check: {title}")

    return web.json_response({"ok": True, "title": title, "causes": causes, "emergency": bool(row.get("emergency"))})


async def api_reminders_get(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    return web.json_response({"ok": True, "items": user_reminders.get(user_id, [])})


async def api_reminders_add(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    body = await request.json()

    reminder = {
        "type": body.get("type", "reminder_one_time").strip(),
        "text": body.get("text", "").strip(),
        "date": body.get("date", "").strip(),
        "days": body.get("days", "").strip(),
        "time": body.get("time", "").strip(),
        "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
    }
    if not reminder["text"] or not reminder["time"]:
        return _json_error("Reminder text and time are required")

    user_reminders.setdefault(user_id, []).append(reminder)
    add_to_history(user_id, f"⏰ Added reminder: {reminder['text']}")
    return web.json_response({"ok": True, "item": reminder})


async def api_ads_get(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    only_mine = request.query.get("mine") == "1"

    if only_mine:
        items = user_ads.get(user_id, [])
    else:
        items = []
        for ads in user_ads.values():
            items.extend(ads)
        items = items[-50:]

    return web.json_response({"ok": True, "items": items})


async def api_ads_add(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    body = await request.json()

    ad = {
        "title": body.get("title", "").strip(),
        "text": body.get("text", "").strip(),
        "price": body.get("price", "").strip(),
        "contact": body.get("contact", "").strip(),
        "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "user_id": user_id,
    }

    if not ad["title"] or not ad["text"] or not ad["contact"]:
        return _json_error("Title, description and contact are required")

    user_ads.setdefault(user_id, []).append(ad)
    add_to_history(user_id, f"📢 Added ad: {ad['title']}")
    return web.json_response({"ok": True, "item": ad})


async def api_directions(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    lang = _get_lang(user_id)
    items = [{"idx": idx, "name": _direction_name(lang, idx)} for idx in range(len(DIRECTIONS))]
    return web.json_response({"ok": True, "items": items})


async def api_vets(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])

    direction_idx_raw = request.query.get("direction_idx")
    page = max(0, int(request.query.get("page", "0")))
    per_page = 6

    vets = [(vet_id, profile) for vet_id, profile in vet_profiles.items() if vet_id != user_id]

    if direction_idx_raw is not None and direction_idx_raw != "":
        try:
            idx = int(direction_idx_raw)
            aliases = _direction_aliases(idx)
        except (ValueError, IndexError):
            return _json_error("Invalid direction index")

        vets = [
            item
            for item in vets
            if any(alias in (item[1].get("vet_specialization", "").lower()) for alias in aliases)
        ]

    start = page * per_page
    chunk = vets[start : start + per_page]
    items = []
    for vet_id, profile in chunk:
        items.append(
            {
                "id": vet_id,
                "name": profile.get("vet_name", "Veterinarian"),
                "specialization": profile.get("vet_specialization", "Specialist"),
            }
        )

    return web.json_response(
        {
            "ok": True,
            "items": items,
            "page": page,
            "has_prev": page > 0,
            "has_next": start + per_page < len(vets),
            "total": len(vets),
        }
    )


async def api_vet_contact(request: web.Request) -> web.Response:
    _require_user(request)
    try:
        vet_id = int(request.match_info["vet_id"])
    except ValueError:
        return _json_error("Invalid vet id")

    vet = vet_profiles.get(vet_id)
    if not vet:
        return _json_error("Vet not found", status=404)

    return web.json_response(
        {
            "ok": True,
            "item": {
                "id": vet_id,
                "name": vet.get("vet_name", "Veterinarian"),
                "specialization": vet.get("vet_specialization", "Specialist"),
                "phone": vet.get("vet_phone", "-"),
                "telegram": vet.get("vet_telegram", "-"),
                "price": vet.get("vet_consultation_price", "-"),
                "info": vet.get("vet_info", "-"),
            },
        }
    )


async def api_history_get(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    return web.json_response({"ok": True, "items": user_history.get(user_id, [])[-50:]})


async def api_history_clear(request: web.Request) -> web.Response:
    user = _require_user(request)
    user_id = int(user["id"])
    user_history[user_id] = []
    add_to_history(user_id, "🗑️ History cleared")
    return web.json_response({"ok": True})


def create_webapp_server(bot_token: str) -> web.Application:
    app = web.Application()
    app["bot_token"] = bot_token

    app.router.add_get("/webapp", index_page)
    app.router.add_get("/webapp/{name}", static_file)

    app.router.add_get("/webapp/api/bootstrap", api_bootstrap)
    app.router.add_post("/webapp/api/language", api_set_language)

    app.router.add_get("/webapp/api/profiles", api_get_profiles)
    app.router.add_put("/webapp/api/profile/pet", api_save_pet_profile)
    app.router.add_put("/webapp/api/profile/vet", api_save_vet_profile)

    app.router.add_get("/webapp/api/directory/{section}/{city}", api_directory)
    app.router.add_get("/webapp/api/news", api_news)
    app.router.add_get("/webapp/api/facts/random", api_random_fact)
    app.router.add_get("/webapp/api/feeding/{animal}", api_feeding)

    app.router.add_get("/webapp/api/symptoms/animals", api_symptom_animals)
    app.router.add_get("/webapp/api/symptoms/{animal}", api_symptom_list)
    app.router.add_get("/webapp/api/symptom/{animal}/{idx}", api_symptom_details)

    app.router.add_get("/webapp/api/reminders", api_reminders_get)
    app.router.add_post("/webapp/api/reminders", api_reminders_add)

    app.router.add_get("/webapp/api/ads", api_ads_get)
    app.router.add_post("/webapp/api/ads", api_ads_add)

    app.router.add_get("/webapp/api/vet/directions", api_directions)
    app.router.add_get("/webapp/api/vets", api_vets)
    app.router.add_get("/webapp/api/vet/{vet_id}", api_vet_contact)

    app.router.add_get("/webapp/api/history", api_history_get)
    app.router.add_delete("/webapp/api/history", api_history_clear)

    return app


async def start_webapp_server(bot_token: str):
    host = os.getenv("WEBAPP_HOST", "0.0.0.0")
    port = int(os.getenv("WEBAPP_PORT", "8080"))

    app = create_webapp_server(bot_token)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=host, port=port)
    await site.start()

    print(f"✅ Web App server started: http://{host}:{port}/webapp")
    return runner


async def stop_webapp_server(runner: web.AppRunner | None):
    if runner is not None:
        await runner.cleanup()
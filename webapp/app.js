const tg = window.Telegram?.WebApp;
if (tg) {
  tg.ready();
  tg.expand();
}

const appEl = document.getElementById("app");
const userLabel = document.getElementById("userLabel");
const backBtn = document.getElementById("backBtn");

const state = {
  bootstrap: null,
  stack: [],
};

const UI = {
  ru: {
    menu: "Главное меню",
    profile: "Профиль",
    places: "Клиники / Аптеки / Приюты",
    symptoms: "Проверка симптомов",
    feeding: "Кормление",
    reminders: "Напоминания",
    ads: "Объявления",
    news: "Новости и факты",
    vet: "Чат с ветеринаром",
    history: "История",
    language: "Язык",
  },
  en: {
    menu: "Main menu",
    profile: "Profile",
    places: "Clinics / Pharmacies / Shelters",
    symptoms: "Symptoms",
    feeding: "Feeding",
    reminders: "Reminders",
    ads: "Ads",
    news: "News & facts",
    vet: "Vet chat",
    history: "History",
    language: "Language",
  },
  uz: {
    menu: "Asosiy menyu",
    profile: "Profil",
    places: "Klinikalar / Dorixonalar / Boshpanalar",
    symptoms: "Simptomlar",
    feeding: "Oziqlantirish",
    reminders: "Eslatmalar",
    ads: "E'lonlar",
    news: "Yangilik va faktlar",
    vet: "Veterinar chat",
    history: "Tarix",
    language: "Til",
  },
};

function t(key) {
  const lang = state.bootstrap?.lang || "ru";
  return UI[lang]?.[key] || UI.ru[key] || key;
}

async function api(path, options = {}) {
  const initData = tg?.initData || "";
  const resp = await fetch(`/webapp/api${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-Telegram-Init-Data": initData,
      ...(options.headers || {}),
    },
  });

  const payload = await resp.json().catch(() => ({}));
  if (!resp.ok || payload.ok === false) {
    throw new Error(payload.error || `Request failed: ${resp.status}`);
  }
  return payload;
}

function showError(err) {
  appEl.innerHTML = `<div class="card"><b>Ошибка:</b> ${err.message}</div>`;
}

function setBackVisible(visible) {
  backBtn.classList.toggle("hidden", !visible);
}

function openView(name, params = {}, push = true) {
  if (push) state.stack.push({ name, params });
  setBackVisible(state.stack.length > 1);

  const renderer = views[name];
  if (!renderer) return;
  renderer(params).catch(showError);
}

backBtn.addEventListener("click", () => {
  if (state.stack.length <= 1) return;
  state.stack.pop();
  const prev = state.stack[state.stack.length - 1];
  openView(prev.name, prev.params, false);
});

const views = {
  home: async () => {
    appEl.innerHTML = `
      <section class="card">
        <h2>${t("menu")}</h2>
        <div class="grid" id="homeGrid"></div>
      </section>
    `;

    const actions = [
      ["profile", "👤"],
      ["places", "📍"],
      ["symptoms", "🩺"],
      ["feeding", "🍖"],
      ["reminders", "⏰"],
      ["ads", "📢"],
      ["news", "📰"],
      ["vet", "💬"],
      ["history", "📋"],
      ["language", "🌍"],
    ];

    const grid = document.getElementById("homeGrid");
    for (const [key, icon] of actions) {
      const btn = document.createElement("button");
      btn.innerText = `${icon} ${t(key)}`;
      btn.addEventListener("click", () => openView(key));
      grid.appendChild(btn);
    }
  },

  profile: async () => {
    const data = await api("/profiles");
    const cities = state.bootstrap.cities.map((c) => `<option value="${c.name}">${c.name}</option>`).join("");

    appEl.innerHTML = `
      <section class="card">
        <h2>👤 ${t("profile")}</h2>
        <small>Поля совпадают с ботом.</small>
      </section>

      <section class="card">
        <h3>Профиль питомца</h3>
        <form id="petForm">
          <input name="owner_name" placeholder="Имя владельца" value="${data.pet_profile.owner_name || ""}" required />
          <input name="owner_phone" placeholder="Телефон" value="${data.pet_profile.owner_phone || ""}" />
          <input list="cities" name="city" placeholder="Город" value="${data.pet_profile.city || ""}" />
          <input name="pet_name" placeholder="Имя питомца" value="${data.pet_profile.pet_name || ""}" required />
          <input name="pet_type" placeholder="Вид" value="${data.pet_profile.pet_type || ""}" />
          <input name="pet_breed" placeholder="Порода" value="${data.pet_profile.pet_breed || ""}" />
          <input name="pet_age" placeholder="Возраст" value="${data.pet_profile.pet_age || ""}" />
          <input name="pet_weight" placeholder="Вес" value="${data.pet_profile.pet_weight || ""}" />
          <input name="pet_color" placeholder="Цвет" value="${data.pet_profile.pet_color || ""}" />
          <textarea name="allergies" placeholder="Аллергии">${data.pet_profile.allergies || ""}</textarea>
          <textarea name="diseases" placeholder="Болезни">${data.pet_profile.diseases || ""}</textarea>
          <textarea name="vaccinations" placeholder="Вакцинации">${data.pet_profile.vaccinations || ""}</textarea>
          <button class="primary" type="submit">Сохранить профиль питомца</button>
        </form>
      </section>

      <section class="card">
        <h3>Профиль ветеринара</h3>
        <form id="vetForm">
          <input name="vet_name" placeholder="ФИО" value="${data.vet_profile.vet_name || ""}" required />
          <input name="vet_phone" placeholder="Телефон" value="${data.vet_profile.vet_phone || ""}" />
          <input list="cities" name="vet_city" placeholder="Город" value="${data.vet_profile.vet_city || ""}" />
          <input name="vet_specialization" placeholder="Специализация" value="${data.vet_profile.vet_specialization || ""}" />
          <input name="vet_experience" placeholder="Опыт" value="${data.vet_profile.vet_experience || ""}" />
          <input name="vet_education" placeholder="Образование" value="${data.vet_profile.vet_education || ""}" />
          <input name="vet_telegram" placeholder="Telegram username" value="${data.vet_profile.vet_telegram || ""}" />
          <input name="vet_consultation_price" placeholder="Цена консультации" value="${data.vet_profile.vet_consultation_price || ""}" />
          <textarea name="vet_info" placeholder="О себе">${data.vet_profile.vet_info || ""}</textarea>
          <button class="primary" type="submit">Сохранить профиль ветеринара</button>
        </form>
      </section>

      <datalist id="cities">${cities}</datalist>
    `;

    document.getElementById("petForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const body = Object.fromEntries(new FormData(e.target).entries());
      await api("/profile/pet", { method: "PUT", body: JSON.stringify(body) });
      tg?.showAlert("Профиль питомца сохранён");
    });

    document.getElementById("vetForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const body = Object.fromEntries(new FormData(e.target).entries());
      await api("/profile/vet", { method: "PUT", body: JSON.stringify(body) });
      tg?.showAlert("Профиль ветеринара сохранён");
    });
  },

  places: async () => {
    const cities = state.bootstrap.cities;
    const cityOptions = cities.map((c) => `<option value="${c.key}">${c.name}</option>`).join("");

    appEl.innerHTML = `
      <section class="card">
        <h2>📍 ${t("places")}</h2>
        <form id="placesForm" class="row">
          <select name="section">
            <option value="clinics">Клиники</option>
            <option value="pharmacies">Аптеки</option>
            <option value="shelters">Приюты</option>
            <option value="pet_shop">Зоомагазин</option>
          </select>
          <select name="city">${cityOptions}</select>
          <button class="primary" type="submit">Показать</button>
        </form>
      </section>
      <section class="card" id="placesResult">Выберите раздел и город.</section>
    `;

    document.getElementById("placesForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const form = Object.fromEntries(new FormData(e.target).entries());
      const data = await api(`/directory/${form.section}/${form.city}`);
      const result = document.getElementById("placesResult");

      if (!data.items.length) {
        result.innerHTML = `<b>Нет данных для выбранного города.</b><br/><a href="${data.map_link}" target="_blank">Открыть карту</a>`;
        return;
      }

      result.innerHTML = data.items.map((x) => `<div class="list-item">${x}</div>`).join("") + `<a href="${data.map_link}" target="_blank">Показать на карте</a>`;
    });
  },

  symptoms: async () => {
    const animals = await api("/symptoms/animals");
    appEl.innerHTML = `
      <section class="card">
        <h2>🩺 ${t("symptoms")}</h2>
        <div id="animals"></div>
      </section>
      <section class="card" id="symptomsList">Выберите животное.</section>
      <section class="card" id="symptomDetails">Выберите симптом.</section>
    `;

    const animalsEl = document.getElementById("animals");
    animals.items.forEach((animal) => {
      const btn = document.createElement("button");
      btn.textContent = animal.label;
      btn.style.margin = "0 6px 6px 0";
      btn.addEventListener("click", async () => {
        const rows = await api(`/symptoms/${animal.id}`);
        document.getElementById("symptomsList").innerHTML = rows.items
          .map((item) => `<button data-animal="${animal.id}" data-idx="${item.idx}" class="sym-btn">${item.title}</button>`)
          .join(" ");

        document.querySelectorAll(".sym-btn").forEach((el) => {
          el.addEventListener("click", async () => {
            const d = await api(`/symptom/${el.dataset.animal}/${el.dataset.idx}`);
            document.getElementById("symptomDetails").innerHTML = `
              <h3>${d.title}</h3>
              ${d.causes.map((c) => `<div class="list-item">• ${c}</div>`).join("")}
              ${d.emergency ? `<p class="emergency">⚠️ Экстренный симптом</p>` : ""}
            `;
          });
        });
      });
      animalsEl.appendChild(btn);
    });
  },

  feeding: async () => {
    const keys = ["dog", "cat", "bird", "rodent", "fish", "reptile", "cow", "sheep"];
    appEl.innerHTML = `
      <section class="card">
        <h2>🍖 ${t("feeding")}</h2>
        <div id="feedButtons"></div>
      </section>
      <section class="card" id="feedResult">Выберите тип животного.</section>
    `;

    const holder = document.getElementById("feedButtons");
    keys.forEach((k) => {
      const btn = document.createElement("button");
      btn.textContent = k;
      btn.style.margin = "0 6px 6px 0";
      btn.addEventListener("click", async () => {
        const data = await api(`/feeding/${k}`);
        document.getElementById("feedResult").innerHTML = data.text;
      });
      holder.appendChild(btn);
    });
  },

  reminders: async () => {
    appEl.innerHTML = `
      <section class="card">
        <h2>⏰ ${t("reminders")}</h2>
        <form id="remForm">
          <input name="text" placeholder="Текст напоминания" required />
          <select name="type">
            <option value="reminder_one_time">Один раз</option>
            <option value="reminder_daily">Ежедневно</option>
            <option value="reminder_weekly">Еженедельно</option>
          </select>
          <input name="date" placeholder="Дата (ДД.ММ.ГГГГ) для one-time" />
          <input name="days" placeholder="Дни (для weekly)" />
          <input name="time" placeholder="Время ЧЧ:ММ" required />
          <button class="primary" type="submit">Добавить</button>
        </form>
      </section>
      <section class="card" id="remList"></section>
    `;

    async function refresh() {
      const data = await api("/reminders");
      document.getElementById("remList").innerHTML = data.items.length
        ? data.items.map((r) => `<div class="list-item"><b>${r.text}</b><br/>${r.type} | ${r.date || r.days || "-"} ${r.time}</div>`).join("")
        : "Напоминаний пока нет.";
    }

    await refresh();

    document.getElementById("remForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const body = Object.fromEntries(new FormData(e.target).entries());
      await api("/reminders", { method: "POST", body: JSON.stringify(body) });
      e.target.reset();
      await refresh();
    });
  },

  ads: async () => {
    appEl.innerHTML = `
      <section class="card">
        <h2>📢 ${t("ads")}</h2>
        <form id="adForm">
          <input name="title" placeholder="Заголовок" required />
          <textarea name="text" placeholder="Описание" required></textarea>
          <input name="price" placeholder="Цена" />
          <input name="contact" placeholder="Контакт" required />
          <button class="primary" type="submit">Опубликовать</button>
        </form>
      </section>
      <section class="card">
        <div class="row">
          <button id="allAds">Все объявления</button>
          <button id="myAds">Мои объявления</button>
        </div>
        <div id="adsList"></div>
      </section>
    `;

    async function loadAds(mine = false) {
      const data = await api(`/ads?mine=${mine ? "1" : "0"}`);
      document.getElementById("adsList").innerHTML = data.items.length
        ? data.items.map((ad) => `<div class="list-item"><b>${ad.title}</b><br/>${ad.text}<br/>💰 ${ad.price || "-"}<br/>📞 ${ad.contact}</div>`).join("")
        : "Объявлений пока нет.";
    }

    await loadAds(false);

    document.getElementById("allAds").addEventListener("click", () => loadAds(false));
    document.getElementById("myAds").addEventListener("click", () => loadAds(true));

    document.getElementById("adForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const body = Object.fromEntries(new FormData(e.target).entries());
      await api("/ads", { method: "POST", body: JSON.stringify(body) });
      e.target.reset();
      await loadAds(true);
    });
  },

  news: async () => {
    const news = await api("/news");
    const fact = await api("/facts/random");

    appEl.innerHTML = `
      <section class="card">
        <h2>📰 ${t("news")}</h2>
        ${news.items.map((n, i) => `<div class="list-item"><b>${i + 1}.</b> ${n}</div>`).join("")}
      </section>
      <section class="card">
        <h3>🎲 Факт</h3>
        <div id="fact">${fact.fact}</div>
        <button id="newFact">Еще факт</button>
      </section>
    `;

    document.getElementById("newFact").addEventListener("click", async () => {
      const next = await api("/facts/random");
      document.getElementById("fact").textContent = next.fact;
    });
  },

  vet: async () => {
    const dirs = await api("/vet/directions");

    appEl.innerHTML = `
      <section class="card">
        <h2>💬 ${t("vet")}</h2>
        <select id="dirSelect">
          <option value="">Все направления</option>
          ${dirs.items.map((d) => `<option value="${d.idx}">${d.name}</option>`).join("")}
        </select>
        <button id="findVets" class="primary">Найти ветеринаров</button>
      </section>
      <section class="card" id="vetList">Нажмите "Найти ветеринаров".</section>
      <section class="card" id="vetCard">Выберите ветеринара.</section>
    `;

    async function load(page = 0) {
      const direction = document.getElementById("dirSelect").value;
      const url = `/vets?page=${page}${direction !== "" ? `&direction_idx=${direction}` : ""}`;
      const data = await api(url);
      const holder = document.getElementById("vetList");

      if (!data.items.length) {
        holder.innerHTML = "Пока нет доступных ветеринаров.";
        return;
      }

      holder.innerHTML = data.items
        .map((v) => `<button class="vet-btn" data-id="${v.id}">👨‍⚕️ ${v.name} (${v.specialization})</button>`)
        .join(" ");

      const nav = document.createElement("div");
      nav.className = "row";
      if (data.has_prev) {
        const prev = document.createElement("button");
        prev.textContent = "←";
        prev.onclick = () => load(page - 1);
        nav.appendChild(prev);
      }
      if (data.has_next) {
        const next = document.createElement("button");
        next.textContent = "→";
        next.onclick = () => load(page + 1);
        nav.appendChild(next);
      }
      holder.appendChild(nav);

      document.querySelectorAll(".vet-btn").forEach((el) => {
        el.addEventListener("click", async () => {
          const d = await api(`/vet/${el.dataset.id}`);
          const v = d.item;
          const username = (v.telegram || "").replace("@", "");
          document.getElementById("vetCard").innerHTML = `
            <h3>${v.name}</h3>
            <div class="list-item">${v.specialization}</div>
            <div class="list-item">📞 ${v.phone}</div>
            <div class="list-item">💰 ${v.price}</div>
            <div class="list-item">${v.info}</div>
            ${username && username !== "-" ? `<a href="https://t.me/${username}" target="_blank">Открыть чат</a>` : ""}
          `;
        });
      });
    }

    document.getElementById("findVets").addEventListener("click", () => load(0));
  },

  history: async () => {
    const data = await api("/history");
    appEl.innerHTML = `
      <section class="card">
        <h2>📋 ${t("history")}</h2>
        <button id="clearHistory" class="warn">Очистить историю</button>
      </section>
      <section class="card" id="historyList">
        ${data.items.length ? data.items.map((x) => `<div class="list-item">${x}</div>`).join("") : "История пуста."}
      </section>
    `;

    document.getElementById("clearHistory").addEventListener("click", async () => {
      await api("/history", { method: "DELETE" });
      openView("history", {}, false);
    });
  },

  language: async () => {
    appEl.innerHTML = `
      <section class="card">
        <h2>🌍 ${t("language")}</h2>
        <div class="row">
          <button data-lang="ru">🇷🇺 Русский</button>
          <button data-lang="en">🇺🇸 English</button>
          <button data-lang="uz">🇺🇿 O'zbekcha</button>
        </div>
      </section>
    `;

    appEl.querySelectorAll("button[data-lang]").forEach((el) => {
      el.addEventListener("click", async () => {
        await api("/language", { method: "POST", body: JSON.stringify({ lang: el.dataset.lang }) });
        await init(true);
      });
    });
  },
};

async function init(restart = false) {
  state.bootstrap = await api("/bootstrap");
  userLabel.textContent = `${state.bootstrap.user.name} • ${state.bootstrap.lang.toUpperCase()}`;

  if (restart) {
    state.stack = [];
  }

  if (!state.stack.length) {
    openView("home", {}, true);
  } else {
    const current = state.stack[state.stack.length - 1];
    openView(current.name, current.params, false);
  }
}

init().catch(showError);
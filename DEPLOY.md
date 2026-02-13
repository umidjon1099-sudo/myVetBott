# PetHelper Bot — VPS ga deploy qilish

Qisqa va aniq ko‘rsatma: botni Ubuntu serverda Docker orqali ishga tushirish. To‘liq release jarayoni uchun [RELEASE_PLAN.md](RELEASE_PLAN.md) ga qarang.

---

## 1. Talablar

- **OS:** Ubuntu 20.04 LTS yoki yangiroq
- **RAM:** kamida 2GB (4GB tavsiya)
- **Storage:** 20GB SSD
- **Docker** 24.0+
- **Docker Compose** 2.0+ (plugin)
- **Git**

---

## 2. Docker o‘rnatish

```bash
# Tizimni yangilash
sudo apt update && sudo apt upgrade -y

# Docker o‘rnatish
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Docker Compose plugin
sudo apt install -y docker-compose-plugin

# Tekshirish
docker --version
docker compose version

# Foydalanuvchini docker guruhiga qo‘shish
sudo usermod -aG docker $USER
newgrp docker
```

---

## 3. Loyihani serverga olib kelish

```bash
# Masalan: /home/deploy/my_vet_bot
cd /home/deploy   # yoki o‘zingiz tanlagan papka
git clone https://github.com/YOUR_USERNAME/my_vet_bot.git
cd my_vet_bot
```

**Eslatma:** CI/CD ishlatadigan bo‘lsangiz, birinchi marta shu qadamlardan keyin serverda `.env` sozlab, bir martalik `docker compose up -d --build` ishga tushiring. Keyingi yangilanishlar GitHub Actions orqali avtomatik bajariladi.

---

## 4. .env sozlash

```bash
cp .env.example .env
nano .env
```

**Majburiy o‘zgaruvchilar:**

| O‘zgaruvchi | Tavsif |
|-------------|--------|
| `BOT_TOKEN` | Telegram @BotFather dan olingan token |
| `POSTGRES_PASSWORD` | PostgreSQL uchun kuchli parol |

**Muhim:** `docker-compose.yml` da `POSTGRES_USER`, `POSTGRES_DB` va boshqalar ishlatiladi. Agar `.env` da ularni bermasangiz, default qiymatlar qo‘llanadi (`vetbot_user`, `vetbot`). Lokal development uchun `DATABASE_URL` va `REDIS_URL` ni `.env.example` dagi kabi localhost ga sozlang; production da Docker tarmog‘ida `postgres` va `redis` host nomlari ishlatiladi (compose faylida allaqachon berilgan).

**.env misoli (production, serverda):**

```env
BOT_TOKEN=123456:ABC-DEF...
BOT_NAME=PetHelperBot

POSTGRES_DB=vetbot
POSTGRES_USER=vetbot_user
POSTGRES_PASSWORD=your_strong_password_here
POSTGRES_PORT=5432

REDIS_PORT=6379

DEBUG=False
LOG_LEVEL=INFO
```

---

## 5. Birinchi ishga tushirish

**5.1.** Avvalo PostgreSQL ni ishga tushiring:

```bash
docker compose up -d postgres
```

**5.2.** PostgreSQL tayyor bo‘lishini kuting, keyin Redis va botni ishga tushiring:

```bash
docker compose up -d --build
```

**Alembic migrations:** Agar loyihada `alembic.ini` va `alembic/versions/` mavjud bo‘lsa, migratsiyalarni qo‘llash uchun:

```bash
docker compose run --rm bot alembic upgrade head
```

Agar Alembic hali loyihada ishlatilmasa (migrations papkasi yo‘q), bu qadamni o‘tkazib yuboring.

---

## 6. Tekshirish

```bash
# Konteynerlar holati
docker compose ps

# Bot loglari
docker compose logs -f bot
```

Telegram da botga `/start` yuborib ishlashini tekshiring.

---

## 7. Keyingi yangilanishlar

**Qo‘lda (CI/CD siz):**

```bash
cd /path/to/my_vet_bot
git pull origin main
docker compose up -d --build
```

**CI/CD orqali:** `main` branch ga push qilsangiz, GitHub Actions serverga SSH qilib `git pull` va `docker compose up -d --build` ni avtomatik bajaradi. Buning uchun `.github/workflows/deploy.yml` va GitHub Secrets (`SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY`) sozlangan bo‘lishi kerak — workflow faylidagi izohlarga qarang.

---

## 8. Foydali buyruqlar

```bash
# Loglarni kuzatish
docker compose logs -f bot

# Botni qayta ishga tushirish
docker compose restart bot

# Barcha servislarni to‘xtatish
docker compose down

# Barcha servislarni to‘xtatish va volumelarni o‘chirish (diqqat: ma’lumotlar o‘chadi)
docker compose down -v
```

Maxfiy ma’lumotlar (BOT_TOKEN, parollar) faqat serverdagi `.env` da saqlanadi; ularni GitHub yoki boshqa repoga yubormang.

# PetHelper Bot - Professional Veterinary Assistant

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![aiogram Version](https://img.shields.io/badge/aiogram-3.4+-green.svg)](https://docs.aiogram.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Professional Telegram bot for veterinary services, pet care, and animal health management in Uzbekistan. Features multilingual support (Russian, English, Uzbek), database integration, and modular architecture.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Deployment](#deployment)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

### Multilingual Support
- **3 Languages**: Russian, English, O'zbek
- Easy language switching
- Localized content and UI

### User Profiles
- **Pet Owner Profiles**: Store pet information, medical history
- **Veterinarian Profiles**: Professional profiles with specialization, experience
- Profile management and editing

### Veterinary Services
- **Clinic Finder**: Search veterinary clinics by city
- **Pharmacy Locator**: Find veterinary pharmacies
- **Animal Shelters**: Locate animal shelters and rescue centers
- **Pet Shops**: Directory of pet supply stores

### Consultation Features
- **Vet Chat**: Connect with registered veterinarians
- **Appointment Booking**: Schedule vet appointments
- **Symptom Checker**: AI-powered symptom analysis and recommendations

### Smart Reminders
- Medication reminders
- Vaccination schedules
- Regular procedure notifications
- Customizable reminder types (one-time, daily, weekly, custom)

### Community Features
- **Advertisements**: Post and browse pet-related ads
- **News Feed**: Latest animal care news
- **Pet Facts**: Educational content about animals
- **Feeding Guides**: Detailed nutrition information

### History & Analytics
- Action history tracking
- Medical record storage
- Treatment history

## Architecture

### Project Structure

```
my_vet_bot/
|-- app/
|   |-- __init__.py
|   |-- config.py              # Configuration management
|   |-- database/              # Database layer
|   |   |-- models.py          # SQLAlchemy models
|   |   |-- database.py        # DB connection
|   |   |-- crud.py            # CRUD operations
|   |-- handlers/              # Message handlers
|   |   |-- start.py           # Start command & menu
|   |   |-- profile.py         # Profile management
|   |   |-- clinic.py          # Clinic/pharmacy/shelter
|   |   |-- reminder.py        # Reminder system
|   |   |-- ads.py             # Advertisements
|   |   |-- symptoms.py        # Symptom checker
|   |   |-- other.py           # Other handlers
|   |-- keyboards/             # Keyboard layouts
|   |   |-- main_menu.py       # Main menu
|   |   |-- inline.py         # Inline keyboards
|   |-- locales/              # Translations
|   |   |-- ru.py              # Russian
|   |   |-- en.py              # English
|   |   |-- uz.py              # Uzbek
|   |   |-- loader.py          # Locale loader
|   |-- middlewares/           # Middleware
|   |   |-- language.py        # Language detection
|   |-- services/              # Business logic
|   |   |-- symptom_checker.py # Symptom analysis
|   |   |-- reminder_scheduler.py # Reminder scheduling
|   |-- utils/                 # Utilities
|   |   |-- helpers.py         # Helper functions
|-- logs/                      # Application logs
|-- migrations/                # Alembic migrations
|-- tests/                     # Test suite
|-- .env.example              # Environment template
|-- .dockerignore
|-- .gitignore
|-- docker-compose.yml        # Docker composition
|-- Dockerfile                # Docker image
|-- main.py                   # Application entry point
|-- requirements.txt          # Python dependencies
|-- README.md                 # This file
|-- RELEASE_PLAN.md           # Deployment guide
```

### Technology Stack

- **Bot Framework**: [aiogram 3.4+](https://docs.aiogram.dev/) - Modern async Python framework
- **Database**: [PostgreSQL 15](https://www.postgresql.org/) - Reliable relational database
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) - Powerful ORM with async support
- **Cache**: [Redis 7](https://redis.io/) - In-memory data store (optional)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) - Database migrations
- **Configuration**: [Pydantic Settings](https://docs.pydantic.dev/) - Type-safe config
- **Containerization**: [Docker](https://www.docker.com/) - Easy deployment

## Requirements

### System Requirements
- **Python**: 3.11 or higher
- **PostgreSQL**: 15 or higher
- **Redis**: 7 or higher (optional)
- **Docker**: 24.0+ (for containerized deployment)
- **Docker Compose**: 2.0+

### Python Dependencies
See [requirements.txt](requirements.txt) for full list.

Key dependencies:
- aiogram 3.4.1
- sqlalchemy 2.0.25
- asyncpg 0.29.0
- pydantic 2.6.1
- redis 5.0.1

## Installation

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/my_vet_bot.git
   cd my_vet_bot
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   nano .env
   ```

3. **Start services**
   ```bash
   docker compose up -d --build
   ```

4. **Check logs**
   ```bash
   docker compose logs -f bot
   ```

### Option 2: Manual Installation

1. **Clone and setup**
   ```bash
   git clone https://github.com/yourusername/my_vet_bot.git
   cd my_vet_bot
   ```

2. **Create virtual environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup PostgreSQL**
   ```bash
   # Install PostgreSQL
   sudo apt install postgresql postgresql-contrib
   
   # Create database
   sudo -u postgres psql
   CREATE DATABASE vetbot;
   CREATE USER vetbot_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE vetbot TO vetbot_user;
   \q
   ```

5. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   nano .env
   ```

6. **Initialize database**
   ```bash
   # Run migrations (if using Alembic)
   alembic upgrade head
   
   # Or let the bot create tables automatically
   python main.py
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Bot Configuration
BOT_TOKEN=your_telegram_bot_token_from_botfather

# Database Configuration
DATABASE_URL=postgresql+asyncpg://vetbot_user:password@localhost:5432/vetbot
DATABASE_ECHO=False

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379
REDIS_DB=0

# Application Settings
DEBUG=False
LOG_LEVEL=INFO

# Webhook Settings (optional, for production)
WEBHOOK_ENABLED=False
WEBHOOK_URL=https://your-domain.com
WEBHOOK_PATH=/webhook
WEBHOOK_HOST=0.0.0.0
WEBHOOK_PORT=8000

# Monitoring (optional)
ENABLE_SENTRY=False
SENTRY_DSN=your_sentry_dsn
```

### Getting Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the token and add to `.env`

## Usage

### Starting the Bot

**With Docker:**
```bash
docker compose up -d
```

**Without Docker:**
```bash
python main.py
```

### Bot Commands

- `/start` - Start the bot and show main menu
- `/help` - Show help message
- `/menu` - Show main menu

### Main Features

1. **Profile Management**
   - Create pet owner or veterinarian profile
   - Add pet information
   - Edit profile details

2. **Find Services**
   - Search clinics by city
   - Find pharmacies
   - Locate animal shelters

3. **Health Features**
   - Check symptoms
   - Get recommendations
   - Set medication reminders

4. **Community**
   - Post advertisements
   - Read news
   - Learn pet facts

## Development

### Project Setup for Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install

# Run linting
flake8 app/
black app/

# Run type checking
mypy app/
```

### Database Migrations

Using Alembic for database migrations:

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Adding New Features

1. **Create handler in `app/handlers/`**
   ```python
   # app/handlers/new_feature.py
   from aiogram import Router
   
   router = Router()
   
   @router.message(...)
   async def handle_feature(message):
       # Implementation
   ```

2. **Register router in `main.py`**
   ```python
   from app.handlers import new_feature
   
   dp.include_router(new_feature.router)
   ```

3. **Add translations in locales**
   ```python
   # app/locales/ru.py, en.py, uz.py
   TEXTS = {
       "new_feature_key": "Translated text",
   }
   ```

### Code Style

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions
- Keep functions small and focused
- Use meaningful variable names

## Deployment

### Production Deployment

See [RELEASE_PLAN.md](RELEASE_PLAN.md) for detailed deployment instructions.

**Quick deployment with Docker:**

```bash
# On your VPS server
git clone https://github.com/yourusername/my_vet_bot.git
cd my_vet_bot

# Configure environment
cp .env.example .env
nano .env  # Add production settings

# Start services
docker compose up -d --build

# Check status
docker compose ps
docker compose logs -f
```

### Deployment Platforms

- **VPS**: Use Docker Compose (recommended)
- **Heroku**: Use buildpacks with PostgreSQL addon
- **Railway**: Connect GitHub, add PostgreSQL
- **Render**: Deploy from GitHub with PostgreSQL

### Monitoring

```bash
# View logs
docker compose logs -f bot

# Check resource usage
docker stats

# Database backup
docker compose exec postgres pg_dump -U vetbot_user vetbot > backup.sql
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_handlers.py

# Run with verbose output
pytest -v
```

### Writing Tests

```python
# tests/test_handlers.py
import pytest
from aiogram.types import Message
from app.handlers import start

@pytest.mark.asyncio
async def test_start_command():
    # Test implementation
    pass
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines

- Write tests for new features
- Update documentation
- Follow code style guidelines
- Keep commits atomic and descriptive

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [aiogram](https://docs.aiogram.dev/) - Async Python framework for Telegram Bot API
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit
- [PostgreSQL](https://www.postgresql.org/) - Powerful open source database
- Telegram Bot API documentation

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/my_vet_bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/my_vet_bot/discussions)
- **Email**: your.email@example.com

## Roadmap

### Version 2.1 (Planned)
- [ ] Mini App integration
- [ ] Payment system for consultations
- [ ] Push notifications
- [ ] Admin dashboard
- [ ] Advanced analytics

### Version 2.2 (Future)
- [ ] AI-powered symptom diagnosis
- [ ] Video consultations
- [ ] Pet health tracking charts
- [ ] Integration with vet clinic systems
- [ ] Mobile app (React Native)

## Stats

- **Languages**: 3 (Russian, English, Uzbek)
- **Handlers**: 50+ message handlers
- **Database Tables**: 10 models
- **Features**: 15+ major features
- **Lines of Code**: 5000+ (modular and maintainable)

## Star History

If you find this project useful, please consider giving it a star on GitHub.

---

**Made with care for pet owners and veterinarians**

Last Updated: 2024-02-13 | Version: 2.0.0

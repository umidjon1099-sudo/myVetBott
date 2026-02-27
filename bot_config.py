import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

API_TOKEN = os.getenv("BOT_TOKEN", "8467556633:AAFwl2sXSzq-3SCSHfp0TCSr4vbduIHOOlU") #osnovnoy
# API_TOKEN = os.getenv("BOT_TOKEN", "8489986940:AAHwTZeAUYXFYmi8x6ZBoVIJwtF-jJ3TNqs") #vremeniy

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=storage)

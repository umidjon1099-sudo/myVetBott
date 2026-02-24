import asyncio

from bot_config import bot, dp
from server import run_bot
import handlers  # noqa: F401 - импорт для регистрации всех обработчиков


async def main():
    await run_bot(bot, dp)


if __name__ == "__main__":
    asyncio.run(main())

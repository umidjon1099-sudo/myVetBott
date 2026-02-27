import asyncio
import contextlib

from bot_config import bot, dp
from reminders_notifier import start_reminder_notifier
from server import run_bot
import handlers  # noqa: F401 - импорт для регистрации всех обработчиков


async def main():
    notifier_task = asyncio.create_task(start_reminder_notifier(bot))
    try:
        await run_bot(bot, dp)
    finally:
        notifier_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await notifier_task


if __name__ == "__main__":
    asyncio.run(main())

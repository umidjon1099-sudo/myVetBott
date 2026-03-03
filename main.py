import asyncio
import contextlib

from bot_config import bot, dp
from reminders_notifier import start_reminder_notifier
from server import run_bot
from webapp_server import start_webapp_server, stop_webapp_server
import handlers  # noqa: F401 - импорт для регистрации всех обработчиков


async def main():
    web_runner = await start_webapp_server(bot.token)
    notifier_task = asyncio.create_task(start_reminder_notifier(bot))
    try:
        await run_bot(bot, dp)
    finally:
        notifier_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await notifier_task
        await stop_webapp_server(web_runner)


if __name__ == "__main__":
    asyncio.run(main())

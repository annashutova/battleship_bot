import asyncio

from aiogram.types import BotCommand

from src.integrations.tg_bot import get_dispatcher, get_tg_bot
from src.logger import logger
from src.middleware.metrics import start_metrics_server
from src.on_startup.logger import setup_logger


async def start_polling() -> None:
    bot = get_tg_bot()
    dp = get_dispatcher()
    await bot.set_my_commands(
        [
            BotCommand(command='start', description='Start bot'),
            BotCommand(command='play', description='Create game'),
            BotCommand(command='stats', description='Get statistics'),
        ]
    )

    await bot.delete_webhook()
    logger.info('Deleted webhook')

    setup_logger()

    await start_metrics_server()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_polling())

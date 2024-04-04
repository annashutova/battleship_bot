import asyncio
import os
import sys

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate to the project directory
project_dir = os.path.dirname(current_dir)

# Add the project directory to the Python path
sys.path.append(project_dir)

from aiogram.types import BotCommand

from src.integrations.tg_bot import get_dispatcher, get_tg_bot
from src.logger import logger
from src.on_startup.logger import setup_logger


async def start_polling() -> None:
    bot = get_tg_bot()
    dp = get_dispatcher()
    await bot.set_my_commands(
        [
            BotCommand(command='start', description='Start bot'),
            BotCommand(command='play', description='Create game'),
        ]
    )

    await bot.delete_webhook()
    logger.info('Deleted webhook')

    setup_logger()

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_polling())
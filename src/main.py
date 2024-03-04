import asyncio
import os
import sys

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate to the project directory
project_dir = os.path.dirname(current_dir)

# Add the project directory to the Python path
sys.path.append(project_dir)

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis

from src.handlers.main.router import main_router
from src.handlers.game.router import game_router
from conf.config import settings


bot = Bot(token=settings.BOT_TOKEN)

redis = Redis(
    host='localhost',
    port=6379,
    db=1,
)

storage = RedisStorage(redis)
dp = Dispatcher(storage=storage)

dp.include_routers(main_router, game_router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

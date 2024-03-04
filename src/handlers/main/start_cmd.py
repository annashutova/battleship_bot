import aiohttp
from aiohttp.client_exceptions import ClientResponseError
from aiogram import types
from aiogram.fsm.context import FSMContext

from src.buttons.menu.main import get_keyboard
from conf.config import settings
from src.handlers.main.router import main_router
from aiogram.filters.command import Command

from src.state.game import GameState


@main_router.message(Command('start',))
async def cmd_start(message: types.Message, state: FSMContext):
    timeout = aiohttp.ClientTimeout(total=3)
    connector = aiohttp.TCPConnector()
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        try:
            async with session.post(
                    f'{settings.BACKEND_HOST}/auth/login',
                        json={
                            'username': message.from_user.id,
                        },
            ) as response:
                response.raise_for_status()
                data = await response.json()
        except ClientResponseError:
            return

    access_token = data['access_token']

    await state.set_data({'access_token': access_token})
    await state.set_state(GameState.ship_setup)

    # TODO create instance of game on backend

    await message.answer(
        "Добро пожаловать в морской бой!!\nКак вы хотите расставить свои корабли?",
        reply_markup=get_keyboard()
    )

async def create_game():
    pass
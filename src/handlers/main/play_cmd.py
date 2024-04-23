from aiogram import types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiohttp.client_exceptions import ClientResponseError

from src.buttons.menu.main import get_setup_keyboard
from src.handlers.main.router import main_router
from src.state.game import GameState
from src.utils.request import do_request

from conf.config import settings


@main_router.message(
    Command(
        'play',
    )
)
async def cmd_play(message: types.Message, state: FSMContext) -> None:
    try:
        await do_request(
            f'{settings.BACKEND_HOST}/game/create_game',
        )
    except ClientResponseError:
        await message.answer('Произошла ошибка при создании игры, попробуйте снова.')
        return

    await state.set_state(GameState.ship_setup)
    await message.answer('Как вы хотите расставить свои корабли?', reply_markup=get_setup_keyboard())

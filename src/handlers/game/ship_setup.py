from typing import List

import aiohttp
from aiohttp.client_exceptions import ClientResponseError
from aiogram import types, F
from aiogram.fsm.context import FSMContext

from src.buttons.menu.main import RANDOM_SETUP, MANUAL_SETUP
from conf.config import settings
from src.handlers.game.router import game_router

from src.state.game import GameState
from src.utils.get_boards import get_user_board, get_opponent_board
from src.utils.parsers import parse_coordinates


@game_router.message(F.text == RANDOM_SETUP, GameState.ship_setup)
async def random_setup(message: types.Message, state: FSMContext):
    access_token = (await state.get_data())['access_token']

    # timeout = aiohttp.ClientTimeout(total=3)
    # connector = aiohttp.TCPConnector()
    # async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
    #     try:
    #         async with session.post(
    #                 f'{settings.BACKEND_HOST}/auth/login',
    #                     json={
    #                         'username': message.from_user.id,
    #                     },
    #         ) as response:
    #             response.raise_for_status()
    #             data = await response.json()
    #     except ClientResponseError:
    #         return

    # поле игрока
    board = await get_user_board(access_token)
    await message.answer('Ваше поле:\n\n' + board, reply_markup=types.ReplyKeyboardRemove())

    # поле противника
    opponent_board = await get_opponent_board(access_token)
    await message.answer('Поле противника:\n\n' + opponent_board)
    await message.answer('Куда вы хотите выстрелить?')

    ## здесь меняем стэйт на начало игры
    await state.set_state(GameState.start_game)

@game_router.message(F.text == MANUAL_SETUP)
@game_router.message(GameState.ship_setup)
async def manual_setup(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    access_token = state_data['access_token']

    if message.text != MANUAL_SETUP:
        ship_size = state_data['current_ship']
        try:
            coords = parse_coordinates(message.text, ship_size)
        except ValueError:
            await message.answer(
                f'Вы ввели неправильные координаты для {ship_size}-палубного корабля.\n'
                'Попробуйте снова'
            )
            return

        # отправляем координаты на бэк
        print(coords)

    ship_types = state_data.get('ship_types', None)
    if ship_types is None:
        ship_types = await get_ship_types(access_token)
        await state.update_data({'ship_types': ship_types})

    # выводим поле игрока
    board = await get_user_board(access_token)
    await message.answer('Ваше поле:\n\n' + board, reply_markup=types.ReplyKeyboardRemove())

    if ship_types:

        ship = ship_types.pop(0)
        await state.update_data({'current_ship': ship})
        await state.update_data({'ship_types': ship_types})

        await message.answer(
            f'Куда вы хотите поставить {ship}-палубный корабль?'
        )
        return

    opponent_board = await get_opponent_board(access_token)
    await message.answer('Поле противника:\n\n' + opponent_board)
    await message.answer('Куда вы хотите выстрелить?')

    await state.set_state(GameState.start_game)

async def get_ship_types(access_token: str) -> List[int]:
    # timeout = aiohttp.ClientTimeout(total=3)
    # connector = aiohttp.TCPConnector()

    # async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
    #     try:
    #         async with session.get(
    #                 f'{settings.BACKEND_HOST}/..........', # TODO add url
    #                 headers={'Authorization': f'Bearer {access_token}'},
    #         ) as response:
    #             response.raise_for_status()
    #             data = await response.json()
    #     except Exception:
    #         # TODO logging
    #         return

    # return data['data']
    return [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]


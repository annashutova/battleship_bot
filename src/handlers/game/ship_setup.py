from typing import Any

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiohttp.client_exceptions import ClientResponseError

from src.buttons.menu.main import MANUAL_SETUP, RANDOM_SETUP
from src.handlers.game.router import game_router
from src.state.game import GameState
from src.utils.parsers import parse_board, parse_coordinates
from src.utils.request import do_request

from conf.config import settings


@game_router.message(F.text == RANDOM_SETUP, GameState.ship_setup)
async def random_setup(message: types.Message, state: FSMContext) -> None:
    try:
        data = (
            await do_request(
                f'{settings.BACKEND_HOST}/game/create_random_ships',
            )
        )['data']
    except ClientResponseError:
        await message.answer('Произошла ошибка, попробуйте еще раз.')
        return

    await message.answer('Ваше поле:\n\n' + parse_board(data['player_board']))
    await message.answer(
        'Поле противника:\n\n' + parse_board(data['ai_board']), reply_markup=types.ReplyKeyboardRemove()
    )
    await message.answer('Куда вы хотите выстрелить?\n' 'Пример координаты поля: A6 или a6')

    await state.set_state(GameState.start_game)


@game_router.message(F.text == MANUAL_SETUP, GameState.ship_setup)
async def initial_manual_setup(message: types.Message, state: FSMContext) -> None:
    state_data = await state.get_data()

    try:
        data = (
            await do_request(
                f'{settings.BACKEND_HOST}/game/player_board',
                method='GET',
            )
        )['data']
    except ClientResponseError:
        await message.answer('Произошла ошибка, попробуйте еще раз.')
        return

    await _common_ship_setup(message, state, state_data, data)


@game_router.message(GameState.ship_setup)
async def manual_setup(message: types.Message, state: FSMContext) -> None:
    state_data = await state.get_data()

    ship_size = state_data['current_ship']
    try:
        coords = parse_coordinates(message.text, ship_size)
    except ValueError:
        await message.answer(
            f'Вы ввели неправильные координаты для {ship_size}-палубного корабля.\n' 'Попробуйте снова'
        )
        return

    # отправляем координаты на бэк
    try:
        data = (
            await do_request(
                f'{settings.BACKEND_HOST}/game/create_ship',
                json_data={'coords': coords},
            )
        )['data']
    except ClientResponseError:
        await message.answer(
            f'Вы ввели неправильные координаты для {ship_size}-палубного корабля.\n' 'Попробуйте снова'
        )
        return

    await _common_ship_setup(message, state, state_data, data)


async def _common_ship_setup(
    message: types.Message,
    state: FSMContext,
    state_data: dict[str, Any],
    response_data: dict[str, Any],
) -> None:
    # выводим поле игрока
    await message.answer(
        'Ваше поле:\n\n' + parse_board(response_data['player_board']),
        reply_markup=types.ReplyKeyboardRemove(),
    )

    ship_types = state_data.get('ship_types')
    if ship_types is None:
        try:
            ship_types = (
                await do_request(
                    f'{settings.BACKEND_HOST}/game/setup_rules',
                    method='GET',
                )
            )[
                'data'
            ]['ship_types']
        except ClientResponseError:
            await message.answer('Произошла ошибка, попробуйте еще раз.')
            return

        await state.update_data({'ship_types': ship_types})

    if ship_types:
        ship = ship_types.pop(0)
        await state.update_data({'current_ship': ship, 'ship_types': ship_types})

        await message.answer(
            f'Куда вы хотите поставить {ship}-палубный корабль?\n' 'Пример для 2-палубного корабля: C3D3 или c3d3'
        )
        return

    # выводим поле противника
    try:
        data = (
            await do_request(
                f'{settings.BACKEND_HOST}/game/opponent_board',
                method='GET',
            )
        )['data']
    except ClientResponseError:
        await message.answer('Произошла ошибка, попробуйте еще раз.')
        return
    await message.answer('Поле противника:\n\n' + parse_board(data['ai_board']))
    await message.answer('Куда вы хотите выстрелить?\n' 'Пример координаты поля: A6 или a6')

    await state.set_state(GameState.start_game)

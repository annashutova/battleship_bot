from typing import Tuple

import aiohttp
from aiohttp.client_exceptions import ClientResponseError
from aiogram import types, F
from aiogram.fsm.context import FSMContext

from conf.config import settings
from src.handlers.game.router import game_router

from src.state.game import GameState
from src.utils.get_boards import get_user_board, get_opponent_board
from src.utils.parsers import parse_coordinates


@game_router.message(GameState.start_game)
async def start_game(message: types.Message, state: FSMContext):
    access_token = (await state.get_data())['access_token']

    # здесь обрабатываем координату
    try:
        coord = parse_coordinates(message.text)
    except ValueError:
        await message.answer(
            'Вы ввели неправильную координату для выстрела.\n'
            'Попробуйте еще раз'
        )
        return

    # посылаем координату на бэк
    strike_result = await strike_coord(*coord)
    # выводим поле противника с результатом выстрела
    board = await get_opponent_board(access_token)

    match strike_result:
        case 1:
            answer = 'О нет! Это промах, капитан...'
        case 3:
            answer = 'Мы их подбили, так держать, капитан!💣'
        case 5:
            answer = 'Корабль противника потоплен!🍾'

    await message.answer(
        f'{board}\n{answer}'
    )

    # проверяем на конец игры

    # если попадание, запрашиваем еще координату
    if strike_result == 1 or strike_result == 5:
        await message.answer('Поле противника:\n\n' + board)
        await message.answer('Куда вы хотите выстрелить?')

    # если промах, ход делает противник
    else:
        while True:
            #делаем запрос на бэк, получаем результат: попадание или нет
            ai_strike = await 
    # выводится поле юзера с результатом выстрела
    
    # продолжается, пока у одного из игроков не закончатся корабли
    
async def strike_coord(coord: Tuple[int, int]) -> int:
    # посылаем координату на бэк
    print(*coord)

    # получаем ответ
    # 1-промах
    # 3-попадание
    # 0-корабль потоплен
    return 0

import asyncio

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiohttp.client_exceptions import ClientResponseError

from src.handlers.game.router import game_router
from src.state.game import GameState
from src.utils.config import HitStatus
from src.utils.parsers import parse_board, parse_coordinates
from src.utils.request import do_request

from conf.config import settings


@game_router.message(GameState.start_game)
async def start_game(message: types.Message, state: FSMContext) -> None:
    # здесь обрабатываем координату
    try:
        coord = parse_coordinates(message.text)[0]
    except ValueError:
        await message.answer('Вы ввели неправильную координату для выстрела.\n' 'Попробуйте еще раз')
        return

    # посылаем координату на бэк
    try:
        data = (
            await do_request(
                f'{settings.BACKEND_HOST}/game/player_strike',
                json_data={'coord': coord},
            )
        )['data']
    except ClientResponseError:
        await message.answer('Вы ввели неправильную координату для выстрела.\nПопробуйте снова')
        return

    strike_status = data['status']
    ai_board = parse_board(data['ai_board'])

    # выводим поле противника с результатом выстрела
    match strike_status:
        case HitStatus.MISS.value:
            answer = 'О нет! Это промах, капитан...'
        case HitStatus.HIT.value:
            answer = 'Мы их подбили, так держать, капитан!💣'
        case HitStatus.DESTROYED.value:
            answer = 'Корабль противника потоплен!🍾'

    await message.answer(f'Поле противника:\n\n{ai_board}\n{answer}')

    # проверяем на конец игры
    if data['finished']:
        # await message.answer(render('end_feedback/win.jinja2'))
        await message.answer('Вы выиграли!')
        await state.set_state(None)

        try:
            await do_request(
                f'{settings.BACKEND_HOST}/stats/save_data',
            )
        except ClientResponseError:
            await message.answer('Ошибка при сохранении данных игры')
        return

    # если попадание, запрашиваем еще координату
    if strike_status in (HitStatus.HIT.value, HitStatus.DESTROYED.value):
        await message.answer('Куда вы хотите выстрелить?\n' 'Пример координаты поля: A6 или a6')
        return
    # если промах, ход делает ии
    else:
        ai_status = HitStatus.HIT.value
        while ai_status in (HitStatus.HIT.value, HitStatus.DESTROYED.value):
            await asyncio.sleep(0)
            # делаем запрос на бэк, получаем результат
            try:
                data = (
                    await do_request(
                        f'{settings.BACKEND_HOST}/game/ai_strike',
                    )
                )['data']
            except ClientResponseError:
                continue

            ai_status = data['status']
            player_board = parse_board(data['player_board'])

            # выводится поле юзера с результатом выстрела
            match ai_status:
                case HitStatus.MISS.value:
                    answer = 'Противник промахнулся!🍾'
                case HitStatus.HIT.value:
                    answer = 'Наш корабль подбит, капитан!💣'
                case HitStatus.DESTROYED.value:
                    answer = 'Палундра! Корабль потоплен!⚓️'

            await message.answer(f'Ваше поле:\n\n{player_board}\n{answer}')

            # проверяем на конец игры
            if data['finished']:
                # await message.answer(render('end_feedback/loss.jinja2'))
                await message.answer('Вы проиграли!')
                await state.set_state(None)

                try:
                    await do_request(
                        f'{settings.BACKEND_HOST}/stats/save_data',
                    )
                except ClientResponseError:
                    await message.answer('Ошибка при сохранении данных игры')
                return

    # продолжается, пока у одного из игроков не закончатся корабли
    await message.answer(f'Поле противника:\n\n{ai_board}')
    await message.answer('Куда вы хотите выстрелить?\n' 'Пример координаты поля: A6 или a6')
    return

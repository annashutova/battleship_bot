from typing import Any, Dict

from aiogram import F, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiohttp.client_exceptions import ClientResponseError

from src.buttons.menu.stats import get_stats_buttons
from src.handlers.main.router import main_router
from src.logger import logger
from src.template.render import render
from src.utils.request import do_request

from conf.config import settings


@main_router.message(
    Command(
        'stats',
    )
)
async def cmd_stats(message: types.Message, state: FSMContext) -> None:
    await message.answer('За какой период вы хотите посмотреть статистику?', reply_markup=get_stats_buttons())


@main_router.callback_query(F.data == 'day')
async def get_day_stats(callback: types.CallbackQuery, state: FSMContext) -> None:
    match callback.message:
        case types.Message():
            if stats := await get_game_stats(1):
                stats['period'] = 'день'
                await callback.message.answer(render('statistics/stats.jinja2', **stats))
                await callback.message.delete()
                return
            await callback.message.answer('Не удалось получить статистику за день.')


@main_router.callback_query(F.data == 'week')
async def get_week_stats(callback: types.CallbackQuery, state: FSMContext) -> None:
    match callback.message:
        case types.Message():
            if stats := await get_game_stats(7):
                stats['period'] = 'неделю'
                await callback.message.answer(render('statistics/stats.jinja2', **stats))
                await callback.message.delete()
                return
            await callback.message.answer('Не удалось получить статистику за неделю.')


@main_router.callback_query(F.data == 'month')
async def get_month_stats(callback: types.CallbackQuery, state: FSMContext) -> None:
    match callback.message:
        case types.Message():
            if stats := await get_game_stats(30):
                stats['period'] = 'месяц'
                await callback.message.answer(render('statistics/stats.jinja2', **stats))
                await callback.message.delete()
                return
            await callback.message.answer('Не удалось получить статистику за месяц.')


async def get_game_stats(period: int) -> Dict[str, Any] | None:
    try:
        data = (await do_request(f'{settings.BACKEND_HOST}/stats/get_stats', params={'period': period}, method='GET'))[
            'data'
        ]
    except ClientResponseError:
        logger.exception('Error getting game stats')
        return None
    return data

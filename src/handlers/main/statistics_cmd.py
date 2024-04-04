from aiohttp.client_exceptions import ClientResponseError
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from src.buttons.menu.stats import get_stats_buttons
from conf.config import settings
from src.handlers.main.router import main_router
from src.utils.request import do_request
from src.state.stats import StatsState

from conf.config import settings



@main_router.message(Command('statistics',))
async def cmd_stats(message: types.Message, state: FSMContext):
    access_token = (await state.get_data()).get('access_token', None)
    if access_token is None:
        try:
            data = await do_request(
                f'{settings.TINDER_BACKEND_HOST}/auth/login',
                params={
                    'username': message.from_user.id,
                },
            )
        except ClientResponseError:
            return

    await state.set_data({'access_token': data['access_token']})
    await state.set_state(StatsState.show_stats)

    await message.answer(
        "За какой период вы хотите посмотреть статистику?",
        reply_markup=get_stats_buttons()
    )


@main_router.callback_query(F.data == 'day', StatsState.show_stats)
async def get_day_stats(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # делаем запрос на бэк с периодом запрашиваемой статистики
    stats = await get_game_stats('day', data['access_token']) # пока непонятно в каком формате лучше отправлять период

    await callback.message.answer('Какая-то статистика за день...')
    await callback.message.delete()

@main_router.callback_query(F.data == 'week', StatsState.show_stats)
async def get_week_stats(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # делаем запрос на бэк с периодом запрашиваемой статистики
    stats = await get_game_stats('week', data['access_token']) # пока непонятно в каком формате лучше отправлять период

    await callback.message.answer('Какая-то статистика за неделю...')
    await callback.message.delete()

@main_router.callback_query(F.data == 'month', StatsState.show_stats)
async def get_month_stats(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # делаем запрос на бэк с периодом запрашиваемой статистики
    stats = await get_game_stats('month', data['access_token']) # пока непонятно в каком формате лучше отправлять период

    await callback.message.answer('Какая-то статистика за месяц...')
    await callback.message.delete()

async def get_game_stats(period, access_token: str):
    pass

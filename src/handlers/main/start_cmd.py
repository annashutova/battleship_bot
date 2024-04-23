from aiogram import types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiohttp.client_exceptions import ClientResponseError

from src.handlers.main.router import main_router
from src.logger import logger
from src.utils.request import do_request

from conf.config import settings


@main_router.message(
    Command(
        'start',
    )
)
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    if message.from_user is None:
        await message.answer('Что-то пошло не так')
        logger.error('Without user')
        return

    try:
        data = await do_request(
            f'{settings.BACKEND_HOST}/auth/login',
            json_data={
                'username': message.from_user.id,
            },
        )
    except ClientResponseError:
        logger.exception('Unknown user')
        await message.answer('Не удалось распознать пользователя, зайдите заново.')
        return

    await state.set_data({'access_token': data['access_token']})

    await message.answer(
        'Добро пожаловать в морской бой!!',
    )

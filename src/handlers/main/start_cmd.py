from aiohttp.client_exceptions import ClientResponseError
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from src.handlers.main.router import main_router
from src.utils.request import do_request
from src.logger import logger

from conf.config import settings


@main_router.message(Command('start',))
async def cmd_start(message: types.Message, state: FSMContext):
    try:
        data = await do_request(
            f'{settings.BACKEND_HOST}/auth/login',
            params={
                'username': message.from_user.id,
            },
        )
    except ClientResponseError:
        logger.exception('Unknown user')
        await message.answer('Не удалось распознать пользователя, зайдите заново.')
        return

    await state.set_data({'access_token': data['access_token']})

    await message.answer(
        "Добро пожаловать в морской бой!!",
    )

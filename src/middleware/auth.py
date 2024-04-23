from contextvars import ContextVar
from typing import Any, Awaitable, Callable, Coroutine

from aiogram import BaseMiddleware, Bot
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject

access_token_cxt: ContextVar[str] = ContextVar('access_token_cxt')


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Coroutine[Any, Any, Coroutine[Any, Any, Any]]:
        state: FSMContext = data['state']
        access_token = (await state.get_data()).get('access_token')

        if access_token is None and (not data.get('command') or data['command'].command != 'start'):
            bot: Bot = data['bot']
            await bot.send_message(text='Вы не авторизованы', chat_id=data['event_chat'].id)
            raise SkipHandler('Unauthorized')

        if access_token is not None:
            access_token_cxt.set(access_token)

        return await handler(event, data)

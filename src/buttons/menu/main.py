from aiogram import types


RANDOM_SETUP = 'Рандомно'
MANUAL_SETUP = 'Вручную'


def get_setup_keyboard() -> types.ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=RANDOM_SETUP)],
        [types.KeyboardButton(text=MANUAL_SETUP)],
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)

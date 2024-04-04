from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


DAY = 'День'
WEEK = 'Неделя'
MONTH = 'Месяц'


def get_stats_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=DAY,
            callback_data="day",
        ),
        InlineKeyboardButton(
            text=WEEK,
            callback_data="week",
        ),
        InlineKeyboardButton(
            text=MONTH,
            callback_data="month",
        ),
    )
    return builder.as_markup()

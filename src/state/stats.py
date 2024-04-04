from aiogram.fsm.state import State, StatesGroup


class StatsState(StatesGroup):
    show_stats = State()

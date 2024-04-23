from aiogram.fsm.state import State, StatesGroup


class GameState(StatesGroup):
    ship_setup = State()
    start_game = State()

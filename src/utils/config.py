from enum import Enum

BOARD_STATES = {
    '0': '🌊',
    '1': '⭕️',
    '2': '⬛️',
    '3': '❌',
    '4': '🌊',
    '5': '❌',
}

BOARD_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']


class HitStatus(Enum):
    HIT = 'hit'
    MISS = 'miss'
    DESTROYED = 'destroyed'

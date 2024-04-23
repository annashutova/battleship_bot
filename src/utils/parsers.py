from typing import List, Tuple

from src.utils.config import BOARD_LETTERS, BOARD_STATES


def parse_board(board: List[List[int]]) -> str:
    parsed_board = '     0     1     2     3     4     5     6     7     8     9\n'

    for i, row in enumerate(board):
        letter = BOARD_LETTERS[i]
        parsed_board += f'{letter}  {" ".join([BOARD_STATES[str(elem)] for elem in row])}\n'

    return parsed_board


def parse_coordinates(coords: str | None, ship_size: int | None = None) -> List[Tuple[int, int]]:
    result = []

    if not coords or not coords.isalnum():
        raise ValueError('Invalid input format')

    # Check ship length for the placement
    if ship_size:
        if ship_size * 2 != len(coords):
            raise ValueError('Invalid number of coordinates for this ship')
    # Check for the strike
    else:
        if len(coords) != 2:
            raise ValueError('There must be 1 coordinate for a strike')

    for i in range(0, len(coords), 2):
        letter = coords[i].upper()
        number = int(coords[i + 1])  # raises ValueError if not numeric

        if letter not in BOARD_LETTERS or not 0 <= number <= 9:
            raise ValueError(f'Invalid pair: {coords[i:i+2]}')

        result.append((BOARD_LETTERS.index(letter), number))

    return result

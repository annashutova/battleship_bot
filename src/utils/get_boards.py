from typing import List

import aiohttp
from aiohttp.client_exceptions import ClientResponseError

from src.utils.parsers import parse_board


async def get_user_board(access_token: str) -> str:
    # timeout = aiohttp.ClientTimeout(total=3)
    # connector = aiohttp.TCPConnector()

    # async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
    #     try:
    #         async with session.get(
    #                 f'{settings.BACKEND_HOST}/..........', # TODO add url
    #                 headers={'Authorization': f'Bearer {access_token}'},
    #         ) as response:
    #             response.raise_for_status()
    #             data = await response.json()
    #     except Exception:
    #         # TODO logging
    #         return

    # return data['data']

    board = [
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2, 2, 2, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    return parse_board(board)

async def get_opponent_board(access_token: str) -> str:
     # timeout = aiohttp.ClientTimeout(total=3)
    # connector = aiohttp.TCPConnector()

    # async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
    #     try:
    #         async with session.get(
    #                 f'{settings.BACKEND_HOST}/..........', # TODO add url
    #                 headers={'Authorization': f'Bearer {access_token}'},
    #         ) as response:
    #             response.raise_for_status()
    #             data = await response.json()
    #     except Exception:
    #         # TODO logging
    #         return

    # return data['data']

    board = [
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    return parse_board(board)
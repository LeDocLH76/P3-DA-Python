
import os
from operator import itemgetter
from typing import Literal

from utils.constant import ORDER_ALPHA


def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def crlf() -> None:
    """Line feed"""
    print("")


def input_filter(input: str) -> str:
    """Capitalize

    Args:
        str: string to capitalize

    Return:
        str: first letter capitalized

    """
    if input != "":
        response = input[0].capitalize()
        return response
    return input


def sort_players_by_type(
        sort_type: Literal[1, 2],
        player_dict_list: list[dict]) -> list[dict]:
    """Sort player by sort_type

    Args:
        Literal[1, 2]: ORDER_ALPHA, ORDER_CLASSIFICATION
        list[dict]: list of players dict to sort

    Return:
        list[dict]: list of players dict sorted

    """

    if sort_type == ORDER_ALPHA:
        sorted_player_dict_list = sorted(
            player_dict_list, key=itemgetter('name', 'surname'))
    else:
        sorted_player_dict_list = sorted(player_dict_list, key=itemgetter(
            'classification', 'name', 'surname'))
    return sorted_player_dict_list

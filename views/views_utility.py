# import os
from operator import itemgetter
from typing import Literal

from utils.constant import ORDER_ALPHA


def clear_screen():
    # os.system('cls' if os.name == 'nt' else 'clear')
    print("\033c")
    # print("\033[3J", end="")
    # print("\033[H\033[3J", end="")


def crlf():
    """Line feed"""
    print("\n")


def input_filter(response: str) -> str:
    """Capitalize

    Args:
        str: string to capitalize

    Return:
        str: first letter capitalized

    """
    if response != "":
        response = response[0].capitalize()
    return response


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

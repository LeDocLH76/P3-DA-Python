# import os
from operator import itemgetter
from typing import Literal

from utils.constant import ORDER_ALPHA
from models.player import Player
from models.tournament import Tournament


def clear_screen():
    # os.system('cls' if os.name == 'nt' else 'clear')
    print("\033c")
    # print("\033[3J", end="")
    # print("\033[H\033[3J", end="")


def crlf():
    print("\n")


def input_filter(response: str):
    if response != "":
        response = response[0].capitalize()
    return response


def sort_players_by_type(
        sort_type: Literal[1, 2],
        player_dict_list: list[dict]) -> list[dict]:

    if sort_type == ORDER_ALPHA:
        sorted_player_dict_list = sorted(
            player_dict_list, key=itemgetter('name', 'surname'))
    else:
        sorted_player_dict_list = sorted(player_dict_list, key=itemgetter(
            'classification', 'name', 'surname'))
    return sorted_player_dict_list

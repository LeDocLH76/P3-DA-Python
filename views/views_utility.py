# import os
from operator import itemgetter
from utils import transform_date
from utils.constant import ORDER_ALPHA


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


def sort_players_by_type(sort_type, players):
    if sort_type == ORDER_ALPHA:
        sorted_players = sorted(players, key=itemgetter('name', 'surname'))
    else:
        sorted_players = sorted(players, key=itemgetter(
            'classification', 'name', 'surname'))
    return sorted_players


def build_players_dict(player_document):
    player = {}
    player["id"] = player_document.doc_id
    player["name"] = player_document["name"]
    player["surname"] = player_document["surname"]
    player["gender"] = player_document["gender"]
    player["birth_date"] = transform_date.date_iso2fr(
        player_document["birth_date"])
    player["classification"] = player_document["classification"]
    return player

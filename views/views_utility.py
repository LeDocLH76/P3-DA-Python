import os
from operator import itemgetter
import re


def clear_screen():
    # os.system('cls' if os.name == 'nt' else 'clear')
    print("\033c")
    # print("\033[3J", end="")
    # print("\033[H\033[3J", end="")


def input_filter(response: str):
    if response != "":
        response = response[0].capitalize()
    return response


def date_regex(input_date: str):
    date_patern = re.compile(
        r"^(0?[1-9]|[1-2]\d|3[01])/(0?[1-9]|1[0-2])/(19|20)\d\d$")
    return date_patern.match(input_date)


def classification_regex(input_classification: str):
    classification_patern = re.compile(r"^[1-9]\d{0,5}$")
    return classification_patern.match(input_classification)


def player_id_regex(input_player_id: str):
    player_id_patern = re.compile(r"^[1-9]\d{0,2}$")
    return player_id_patern.match(input_player_id)


def transform_date(date_iso: str) -> str:
    date_list = date_iso.split("-")
    date_list.reverse()
    date_fr = "/".join(date_list)
    return date_fr


def sort_players_by_type(sort_type, players):
    if sort_type == 1:
        sorted_players = sorted(players, key=itemgetter('name', 'surname'))
    else:
        sorted_players = sorted(players, key=itemgetter(
            'classification', 'name', 'surname'))
    return sorted_players


def build_players_list(player_document):
    player = {}
    player["id"] = player_document.doc_id
    player["name"] = player_document["name"]
    player["surname"] = player_document["surname"]
    player["gender"] = player_document["gender"]
    player["birth_date"] = transform_date(player_document["birth_date"])
    player["classification"] = player_document["classification"]
    return player

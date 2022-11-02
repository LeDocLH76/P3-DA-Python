import os
from operator import itemgetter
import re


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def input_filter(response: str):
    if response != "":
        response = response[0].capitalize()
    return response


def date_regex(input_date: str):
    date_regex = re.compile(
        r"^(0?[1-9]|[1-2]\d|3[01])/(0?[1-9]|1[0-2])/(19|20)\d\d$")
    return date_regex.match(input_date)


def classification_regex(input_classification: str):
    classification_regex = re.compile(r"^[1-9]\d{0,5}$")
    return classification_regex.match(input_classification)


def transform_date(date: str):
    date_list = date.split("-")
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
    player["name"] = player_document["name"]
    player["surname"] = player_document["surname"]
    player["gender"] = player_document["gender"]
    player["birth_date"] = transform_date(player_document["birth_date"])
    player["classification"] = player_document["classification"]
    return player

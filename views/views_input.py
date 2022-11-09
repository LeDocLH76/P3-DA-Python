
import re
from utils import filters, transform_date
from utils.constant import (
    PLAYER_NAME_LENGTH,
    PLAYER_SURNAME_LENGTH,
    TOURNAMENT_NAME_LENGTH,
    TOURNAMENT_PLACE_LENGTH,
    TOURNAMENT_DESCRIPTION_LENGTH,
    ROUND_QUANTITY_MIN,
    ROUND_QUANTITY_MAX)
from views import views_utility


def new_player():
    print("Entrer les informations du joueur")
    name = input("Nom ").upper()
    if len(name) > PLAYER_NAME_LENGTH:
        name = name[:PLAYER_NAME_LENGTH-1]

    surname = input("Prénom ").capitalize()
    if len(surname) > PLAYER_SURNAME_LENGTH:
        surname = surname[:PLAYER_SURNAME_LENGTH-1]

    birth_date = None
    while birth_date is None:
        birth_date = input("Date de naissance > jj/mm/aaaa ")
        birth_date = filters.date_regex(birth_date)
    birth_date = transform_date.date_add_0(birth_date.group())

    gender_list = ["M", "F"]
    gender = ""
    while gender not in gender_list:
        gender = input("Genre > M ou F ").upper()

    classification = None
    while classification is None:
        classification = input("Classement > Entier positif non nul ou vide ")
        if classification == "":
            classification = None
            break
        classification = filters.classification_regex(classification)
    if classification is not None:
        classification = int(classification.group())

    player = {
        "name": name,
        "surname": surname,
        "birth_date": birth_date,
        "gender": gender,
        "classification": classification
    }
    return player


def player_choice():
    player_id = None
    while player_id is None:
        response = input(
            "Veuillez choisir un numéro de la liste, ou Q pour annuler --> ")
        if response[0].upper() == "Q":
            return False
        player_id = filters.player_id_regex(response)
    return int(player_id.group())


def tournament_choice(tournament_quantity):
    while True:
        response = re.findall(
            '[0-9]', views_utility.input_filter(
                input("Veuillez choisir un numéro de la liste --> ")))
        if (len(response) > 0
            and int(response[0]) <= tournament_quantity
                and int(response[0]) > 0):
            return int(response[0])


def new_tournament():
    print("Entrer les information du nouveau tournoi")
    name = input(
        f"Nom du tournoi {TOURNAMENT_NAME_LENGTH}car max ").capitalize()
    if len(name) > TOURNAMENT_NAME_LENGTH:
        name = name[:TOURNAMENT_NAME_LENGTH-1]

    place = input(f"Lieu du tournoi {TOURNAMENT_PLACE_LENGTH}car max ")
    if len(place) > TOURNAMENT_PLACE_LENGTH:
        place = place[:TOURNAMENT_PLACE_LENGTH-1]

    date = None
    while date is None:
        date = input("Date du tournoi -> jj/mm/aaaa ")
        date = filters.date_regex(date)
    date = transform_date.date_add_0(date.group())

    time_ctrl_list = ["1", "2", "3"]
    time_ctrl_choice = ""
    while time_ctrl_choice not in time_ctrl_list:
        time_ctrl_choice = input("1: bullet 2: blitz 3: coup rapide ")
    time_ctrl_dict = {
        "1": "Bullet",
        "2": "Blitz",
        "3": "Rapid"
    }
    time_ctrl = time_ctrl_dict[time_ctrl_choice]

    description = input(f"Description {TOURNAMENT_DESCRIPTION_LENGTH}car max ")
    if len(description) > TOURNAMENT_DESCRIPTION_LENGTH:
        description = description[:TOURNAMENT_DESCRIPTION_LENGTH-1]

    tournament_dict = {
        "name": name,
        "place": place,
        "date": date,
        "time_ctrl": time_ctrl,
        "description": description
    }
    return tournament_dict


def change_round_quantity() -> int:
    response = 0
    while (response < ROUND_QUANTITY_MIN) | (response > ROUND_QUANTITY_MAX):
        response = input(f"Entrer le nombre de round {ROUND_QUANTITY_MIN} \
à {ROUND_QUANTITY_MAX} ")
        if not response.isdigit():
            response = 0
        response = int(response)
    return response


def y_or_n() -> bool:
    response_list = ["O", "N"]
    response = ""
    while response not in response_list:
        response = input("Entrer votre choix O ou N --> ").upper()
    return True if response == "O" else False


def wait_for_enter():
    input("Entrer pour continuer")

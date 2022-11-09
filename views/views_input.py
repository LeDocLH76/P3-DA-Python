from views import views_utility
from utility.constant import (
    PLAYER_NAME_LENGTH,
    PLAYER_SURNAME_LENGTH,
    TOURNAMENT_NAME_LENGTH,
    TOURNAMENT_PLACE_LENGTH,
    TOURNAMENT_DESCRIPTION_LENGTH)


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
        birth_date = views_utility.date_regex(birth_date)
    birth_date = birth_date.group()

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
        classification = views_utility.classification_regex(classification)
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


def new_tournament():
    print("Entrer les information du nouveau tournoi")
    name = input("Nom du tournoi 20car max ").capitalize()
    if len(name) > TOURNAMENT_NAME_LENGTH:
        name = name[:TOURNAMENT_NAME_LENGTH-1]

    place = input("Lieu du tournoi 30car max ")
    if len(place) > TOURNAMENT_PLACE_LENGTH:
        place = place[:TOURNAMENT_PLACE_LENGTH-1]

    date = None
    while date is None:
        date = input("Date du tournoi -> jj/mm/aaaa ")
        date = views_utility.date_regex(date)
    date = date.group()

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

    description = input("Description 50car max")
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


def y_or_n():
    response_list = ["O", "N"]
    response = ""
    while response not in response_list:
        response = input("Entrer votre choix O ou N --> ").upper()
    return 1 if response == "O" else 0


def wait_for_enter():
    input("Entrer pour continuer")

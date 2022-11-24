
from utils.filters import (
    number_6_digits_regex,
    date_regex,
    number_3_digits_regex)
from utils.transform_date import date_add_0
from utils.constant import (
    PLAYER_NAME_LENGTH,
    PLAYER_SURNAME_LENGTH,
    TOURNAMENT_NAME_LENGTH,
    TOURNAMENT_PLACE_LENGTH,
    TOURNAMENT_DESCRIPTION_LENGTH,
    ROUND_QUANTITY_MIN,
    ROUND_QUANTITY_MAX)
from views import views_utility


def new_player() -> dict:
    """ Get player's infos from the user

    Return:
        dict: {
            "name": str,
            "surname": str,
            "birt_date": str dd/mm/yyyy,
            "gender": str,
            "classification": int
            }
    """
    print("Entrer les informations du joueur")
    print()
    name = input("Nom ").upper()
    if len(name) > PLAYER_NAME_LENGTH:
        name = name[:PLAYER_NAME_LENGTH - 1]

    surname = input("Prénom ").capitalize()
    if len(surname) > PLAYER_SURNAME_LENGTH:
        surname = surname[:PLAYER_SURNAME_LENGTH - 1]

    birth_date = None
    while birth_date is None:
        birth_date = input("Date de naissance > jj/mm/aaaa ")
        birth_date = date_regex(birth_date)
    birth_date = date_add_0(birth_date.group())

    gender_list = ["M", "F"]
    gender = ""
    while gender not in gender_list:
        gender = input("Genre > M ou F ").upper()

    classification = None
    while classification is None:
        classification = input(
            "Classement > Entier positif non nul vide = 999999 ")
        if classification == "":
            classification = 999999
            break
        classification = number_6_digits_regex(classification)
    if classification != 999999:
        classification = int(classification.group())

    player = {
        "name": name,
        "surname": surname,
        "birth_date": birth_date,
        "gender": gender,
        "classification": classification
    }
    return player


def player_choice() -> int | bool:
    """Ask user for player_id choice

    Return:
        int | bool: player_id or False for no choice

    """
    player_id = None
    while player_id is None:
        response = input(
            "Veuillez choisir un numéro de la liste, ou Q pour annuler --> ")
        if response[0].upper() == "Q":
            return False
        player_id = number_3_digits_regex(response)
    return int(player_id.group())


def add_player_on_tournament_choice() -> int | bool:
    """Ask user for player_id choice, create or exit

    Return:
        int | bool: player_id or False for no choice

    """
    player_id = None
    while player_id is None:
        print("Entrer le numéro du joueur à ajouter \
depuis la liste précendente")
        response = input("C pour en créer un nouveau ou Q pour annuler --> ")
        if response[0].upper() == "Q":
            return False
        if response[0].upper() == "C":
            return True
        player_id = number_3_digits_regex(response)
    return int(player_id.group())


def new_classification() -> int | bool:
    """Input new classification

    Return:
        new_classification(int)

    """
    new_classification = None
    while new_classification is None:
        response = input(
            "Veuillez entrer un classement pour ce joueur, \
ou Q pour annuler --> ")
        if response[0].upper() == "Q":
            return False
        new_classification = number_6_digits_regex(response)
    return int(new_classification.group())


def match_choice() -> int | str:
    """Ask user for match index choice

    Return:
        int | str: match index or Q to exit or C to close round

    """
    response = ""
    while (response != "Q") and (response != "C"):
        print("Choisir le numero du match pour renseigner le score.")
        response = input("Q pour quitter ou C pour cloturer le round ")
        response = views_utility.input_filter(response)
        if response == "C":
            return "C"
        if response == "Q":
            return "Q"
        match_index = number_3_digits_regex(response)
        if match_index is not None:
            return int(match_index.group())


def match_results() -> float:
    """Input score from list["0", ".5", "0.5", "1"]

    Return:
        float: Score could be 0.0, 0.5 or 1.0

    """
    list_scores = ["0", ".5", "0.5", "1"]
    score_str = ""
    while score_str not in list_scores:
        score_str = input(
            "Entrer le score du premier joueur du match 0, 0.5 ou 1 ")
    return float(score_str)


def tournament_choice(tournament_quantity) -> int:
    """Ask user for tournament_id, choice from 1 \
        to 999 and <= tournament_quantity

    Args:
        int: tournament quantity

    Return:
        int: tournament_id

    """

    while True:
        response = input("Veuillez choisir un numéro de la liste --> ")
        match_regex = number_3_digits_regex(response)
        if match_regex is not None:
            tournament_id = int(match_regex.group())
            if tournament_id <= tournament_quantity:
                return tournament_id


def new_tournament() -> dict[str, str]:
    """ Get tournament's infos from the user

    Return:
        dict: {
            name": tournament's name
            "place": tournament's place
            "date": tournament's date
            "time_ctrl": tournament's time_ctrl
            "description": tournament's description
            }
    """

    print("Entrer les information du nouveau tournoi")
    name = input(
        f"Nom du tournoi {TOURNAMENT_NAME_LENGTH}car max ").capitalize()
    if len(name) > TOURNAMENT_NAME_LENGTH:
        name = name[:TOURNAMENT_NAME_LENGTH - 1]

    place = input(f"Lieu du tournoi {TOURNAMENT_PLACE_LENGTH}car max ")
    if len(place) > TOURNAMENT_PLACE_LENGTH:
        place = place[:TOURNAMENT_PLACE_LENGTH - 1]

    date = None
    while date is None:
        date = input("Date du tournoi -> jj/mm/aaaa ")
        date = date_regex(date)
    date = date_add_0(date.group())

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
        description = description[:TOURNAMENT_DESCRIPTION_LENGTH - 1]

    tournament_dict = {
        "name": name,
        "place": place,
        "date": date,
        "time_ctrl": time_ctrl,
        "description": description
    }
    return tournament_dict


def change_round_quantity() -> int:
    """Ask user for new round quantity

    Return:
        int: new quantity between ROUND_QUANTITY_MIN and ROUND_QUANTITY_MAX

    """
    response = 0
    while (response < ROUND_QUANTITY_MIN) | (response > ROUND_QUANTITY_MAX):
        response = input(f"Entrer le nombre de round {ROUND_QUANTITY_MIN} \
à {ROUND_QUANTITY_MAX} ")
        if not response.isdigit():
            response = 0
        response = int(response)
    return response


def y_or_n() -> bool:
    """Ask user for yes or no

    Return:
        bool: Yes = True, no = False

    """
    response_list = ["O", "N"]
    response = ""
    while response not in response_list:
        response = input("Entrer votre choix O ou N --> ").upper()
    return True if response == "O" else False


def wait_for_enter():
    """Wait for user input"""
    input("Entrer pour continuer")

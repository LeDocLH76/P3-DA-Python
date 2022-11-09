import re


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

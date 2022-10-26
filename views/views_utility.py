import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def input_filter(response: str):
    if response != "":
        response = response[0].capitalize()
    return response


def transform_date(date: str):
    date_list = date.split("-")
    date_list.reverse()
    date_fr = "/".join(date_list)
    return date_fr

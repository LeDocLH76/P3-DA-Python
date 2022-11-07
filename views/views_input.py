from views import views_utility


def new_player():
    print("Entrer les informations du joueur")
    name = input("Nom ").upper()
    if len(name) > 20:
        name = name[:20]
    surname = input("Prénom ").capitalize()
    if len(surname) > 20:
        surname = surname[:20]

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


def y_or_n():
    response_list = ["O", "N"]
    response = ""
    while response not in response_list:
        response = input("Entrer votre choix O ou N --> ").upper()
    return 1 if response == "O" else 0


def wait_for_enter():
    input("Entrer pour continuer")

from views import views_utility


def new_player():
    views_utility.clear_screen()
    print("Entrer les informations du nouveau joueur")
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
        "classification": classification
    }
    return player

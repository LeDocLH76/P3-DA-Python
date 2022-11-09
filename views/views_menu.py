
import re

from views import views_utility


def root_menu():
    while True:
        views_utility.clear_screen()
        print("Menu principal")
        print("1. Voir les tournois enregistrés")
        print("2. Voir tous les joueurs enregistrés")
        print("3. Voir les résultats d'un tournoi")
        print("4. Voir les joueurs d'un tournoi")
        print("5. Gestion des joueurs")
        print("6. Reprendre un tournoi en cours")
        print("7. Débuter un nouveau tournoi")
        print("8. Quitter le programme")
        print("Entrer votre choix")
        response = input()
        response = views_utility.input_filter(response)
        if response == "1":
            return 1
        if response == "2":
            return 2
        if response == "3":
            return 3
        if response == "4":
            return 4
        if response == "5":
            return 5
        if response == "6":
            return 6
        if response == "7":
            return 7
        if response == "8":
            return 8


def players_action_choice():
    while True:
        views_utility.clear_screen()
        print("Menu joueurs")
        print("1. Entrer un nouveau joueur")
        print("2. Modifier un joueur")
        print("3. Supprimer un joueur")
        print("4. Voir les joueurs")
        print("5. Retour au menu principal")
        print("Entrer votre choix")
        response = input()
        response = views_utility.input_filter(response)
        if response == "1":
            return 1
        if response == "2":
            print("action 2")
            return 2
        if response == "3":
            print("action 3")
            return 3
        if response == "4":
            print("action 4")
            return 4
        if response == "5":
            return 5


def tournament_choice(tournament_quantity):
    while True:
        response = re.findall(
            '[0-9]', views_utility.input_filter(
                input("Veuillez choisir un numéro de la liste --> ")))
        if (len(response) > 0
            and int(response[0]) <= tournament_quantity
                and int(response[0]) > 0):
            return int(response[0])


def player_choice():
    player_id = None
    while player_id is None:
        response = input(
            "Veuillez choisir un numéro de la liste, ou Q pour annuler --> ")
        if response[0].upper() == "Q":
            return 0
        player_id = views_utility.player_id_regex(response)
    return int(player_id.group())


def sort_choice():
    views_utility.clear_screen()
    print("Type de tri")
    print("1. Alphabetique")
    print("2. Par classement")
    while True:
        print("Entrer votre choix")
        response = input()
        response = views_utility.input_filter(response)
        if response == "1":
            return 1
        if response == "2":
            return 2


def result_type():
    views_utility.clear_screen()
    print("Type de liste")
    print("1. Les rounds du tournoi")
    print("2. Les matchs du tournoi")
    while True:
        print("Entrer votre choix")
        response = input()
        response = views_utility.input_filter(response)
        if response == "1":
            return 1
        if response == "2":
            return 2

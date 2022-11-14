
from typing import Literal
from utils.constant import ORDER_ALPHA, ORDER_CLASSIFICATION
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
        print("5. Retour au menu précédent")
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


def tournament_begin():
    while True:
        views_utility.clear_screen()
        print("1. Débuter le tournoi")
        print("2. Retour au menu principal")
        print("Entrer votre choix")

        response = input()
        response = views_utility.input_filter(response)
        if response == "1":
            return 1
        if response == "2":
            return 2


def sort_choice() -> Literal[1, 2]:
    views_utility.clear_screen()
    print("Type de tri")
    print("1. Alphabetique")
    print("2. Par classement")
    while True:
        print("Entrer votre choix")
        response = input()
        response = views_utility.input_filter(response)
        if response == "1":
            return ORDER_ALPHA
        if response == "2":
            return ORDER_CLASSIFICATION


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

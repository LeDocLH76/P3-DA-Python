
from typing import Literal

from views import views_utility
from utils.constant import (
    ORDER_ALPHA,
    ORDER_CLASSIFICATION,
    RESULT_MATCH,
    RESULT_PLAYER_SCORE,
    RESULT_ROUND
)


def root_menu() -> Literal[1, 2, 3, 4, 5, 6, 7, 8]:
    """Print root menu

    Return:
        int: user choice from 1 to 8

    """
    while True:
        print("Menu principal")
        print()
        print("1. Voir les tournois enregistrés")
        print("2. Voir tous les joueurs enregistrés")
        print("3. Voir les résultats d'un tournoi")
        print("4. Voir les joueurs d'un tournoi")
        print("5. Gestion des joueurs")
        print("6. Reprendre un tournoi en cours")
        print("7. Débuter un nouveau tournoi")
        print("8. Quitter le programme")
        print()
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
        views_utility.clear_screen()
        print()


def players_action_choice() -> Literal[1, 2, 3, 4, 5, 6]:
    """Print submenu player

    Return:
        int: User choice from 1 to 6

    """
    while True:
        views_utility.clear_screen()
        print()
        print("Menu joueurs")
        print()
        print("1. Entrer un nouveau joueur")
        print("2. Modifier un joueur")
        print("3. Supprimer un joueur")
        print("4. Voir les joueurs")
        print("5. Changer le classement d'un joueur")
        print("6. Retour au menu précédent")
        print()
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


def sort_choice() -> Literal[1, 2]:
    """Print submenu sort choice

    Return:
        Literal[1, 2]: ORDER_ALPHA, ORDER_CLASSIFICATION
    """
    print("Type de tri")
    print()
    print("1. Alphabetique")
    print("2. Par classement")
    print()
    while True:
        print("Entrer votre choix")
        response = input()
        response = views_utility.input_filter(response)
        if response == "1":
            return ORDER_ALPHA
        if response == "2":
            return ORDER_CLASSIFICATION


def result_type() -> Literal[1, 2, 3]:
    """Print submenu result choice

    Return
        int: tournament's rounds = 1, tournament's matchs = 2

    """
    print("Type de liste")
    print()
    print("1. Les rounds du tournoi")
    print("2. Les matchs du tournoi")
    print("3. Le classement des joueurs")
    print()
    while True:
        print("Entrer votre choix")
        response = input()
        response = views_utility.input_filter(response)
        if response == "1":
            return RESULT_ROUND
        if response == "2":
            return RESULT_MATCH
        if response == "3":
            return RESULT_PLAYER_SCORE

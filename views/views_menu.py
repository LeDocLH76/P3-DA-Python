
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
        print("5. Reprendre un tournoi en cours")
        print("6. Débuter un nouveau tournoi")
        print("7. Quitter le programme")
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


def players_menu():
    while True:
        views_utility.clear_screen()
        print("Menu joueurs")
        print("1. Entrer un joueur")
        print("2. Modifier un joueur")
        print("3. Supprimer un joueur")
        print("4. Voir les joueurs")
        print("5. Quitter")
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


def tournament_choice(count):
    while True:
        response = re.findall(
            '[0-9]', views_utility.input_filter(
                input("Veuillez choisir un numéro de la liste --> ")))
        if (len(response) > 0
            and int(response[0]) <= count
                and int(response[0]) > 0):
            return int(response[0])


def sort_choice():
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

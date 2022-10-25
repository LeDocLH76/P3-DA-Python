import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def input_filter(response: str):
    if response != "":
        response = response[0].capitalize()
    return response


class views:
    def splash_screen():
        response = ""
        while response != "C":
            # clear_screen()
            print(
                """

            Bienvenue au tournoi d'échec


            Entrer C pour continuer""")
            response = input()
            response = input_filter(response)

    def players_menu():
        while True:
            clear_screen()
            print("Menu principal")
            print("1. Entrer un joueur")
            print("2. Modifier un joueur")
            print("3. Supprimer un joueur")
            print("4. Voir les joueurs")
            print("5. Commencer un tournoi")
            print("Entrer votre choix")
            response = input()
            response = input_filter(response)
            if response == "1":
                return 1
            if response == "2":
                return 2
            if response == "3":
                return 3
            if response == "4":
                return 4
            if response == "5":
                print("La liste des joueurs ne pourra plus être modifiée!")
                print("Continuer? O/N")
                continue_ = input()
                continue_ = input_filter(continue_)
                if continue_ == "O":
                    return 5

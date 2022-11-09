
from controlers.players_controler import players_controler
from controlers.tournament_ctrl import tournament_controler
from views import views_input, views_menu, views_output


def begin():
    # Chess tournament splash screen
    views_output.splash_screen()
    while True:
        # Menu principal
        res_root_menu = views_menu.root_menu()
        # Voir les tournois enregistrés
        if res_root_menu == 1:
            views_output.tournament_list()
            views_input.wait_for_enter()
        # Voir tous les joueurs enregistrés
        if res_root_menu == 2:
            sort_type = views_menu.sort_choice()
            views_output.players_list(sort_type)
            views_input.wait_for_enter()
        # Voir les résultats d'un tournoi
        if res_root_menu == 3:
            tournament_quantity = views_output.tournament_list()
            tournament_id = views_input.tournament_choice(tournament_quantity)
            result_type = views_menu.result_type()
            views_output.tournament_results(tournament_id, result_type)
            views_input.wait_for_enter()
        # Voir les joueurs d'un tournoi
        if res_root_menu == 4:
            tournament_quantity = views_output.tournament_list()
            tournament_id = views_input.tournament_choice(tournament_quantity)
            sort_type = views_menu.sort_choice()
            views_output.tournament_players(tournament_id, sort_type)
            views_input.wait_for_enter()
        # Gestion des joueurs
        if res_root_menu == 5:
            players_controler()
        # Reprendre un tournoi en cours
        if res_root_menu == 6:
            print("Choix 6")

            views_input.wait_for_enter()
        # Débuter un nouveau tournoi
        if res_root_menu == 7:
            print("Choix 7")
            tournament_controler(False)
            views_input.wait_for_enter()
        # Quitter le programme
        if res_root_menu == 8:
            views_output.bye_screen()
            break

            # Entrer les infos du tournoi
            # Entrer la liste des joueurs d'un tournoi
            # Ajouter un joueur
            # Modifier un joueur
            # Supprimer un joueur
            # Lister les joueurs
    # while True:
    #     res_players_menu = views.players_menu()
    #     if res_players_menu == 1:
    #         print("Choix 1")
    #     if res_players_menu == 2:
    #         print("Choix 2")
    #     if res_players_menu == 3:
    #         print("Choix 3")
    #     if res_players_menu == 4:
    #         print("Choix 4")
    #     if res_players_menu == 5:
    #         print("Choix 5")
    #         break
    # Débuter le tournoi
        # Former les paires pour le 1er round
        # Les joueurs jouent ...
        # Entrer les résultats et vérifier complet
            # Voir les résultats du round
            # Modifier les résultats du round
            # Cloturer le round
        # Compteur round
        # Former les paires pour le round suivant
        # Lancer le round suivant
        # Entrer les résultats et vérifier complet
            # Voir les résultats du round
            # Modifier les résultats du round
            # Cloturer le round
        # Si compteur pas atteint, boucler
    # Cloturer tournoi

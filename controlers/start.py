from models import player
from models import match
from models import round
from models import tournament
from views.views import views


def begin():
    """Chess tournament splash screen"""
    views.splash_screen()
    # Menu principal
    # Voir les tournois enregistrés
    # Voir les résultats d'un tournoi
    # Voir les joueurs d'un tournoi
    # Débuter un nouveau tournoi
    # Entrer les infos du tournoi
    # Entrer la liste des joueurs d'un tournoi
    # Ajouter un joueur
    # Modifier un joueur
    # Supprimer un joueur
    # Lister les joueurs
    # Reprendre un tournoi en cours
    while True:
        res_players_menu = views.players_menu()
        if res_players_menu == 1:
            print("Choix 1")
        if res_players_menu == 2:
            print("Choix 2")
        if res_players_menu == 3:
            print("Choix 3")
        if res_players_menu == 4:
            print("Choix 4")
        if res_players_menu == 5:
            print("Choix 5")
            break
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


from utils.constant import ORDER_ALPHA, ROUND_QUANTITY
from views import views_input, views_output, views_utility
from models.tournament import Tournament
from models.db_manager_tournaments import Db_manager_tournament
# from controlers.player_utils import create_player
from controlers.players_controler import players_controler


def tournament_controler(tournament_id):
    # tournoi en cours   status = False
    #   le nombre de round à jouer n'est pas atteint
    #   un round n'est pas cloturés
    # tournoi cloturé    status = True
    #   le nombre de round à jouer est atteint
    #   tous les rounds sont cloturés

    # rounds en cours    valeur = 1 à max

    # round en cours     status = False
    #   la liste de matchs n'est pas cloturée
    # round cloturé      status = True
    #   la liste de matchs est cloturée

    # matchs en cours    status = False
    #   les matchs ne sont pas tous renseignés
    # matchs cloturé     status = True
    #   les matchs sont tous renseignés
    #   l'utilisateur a validé la cloture

    ...
    if tournament_id is False:
        # initialiser un tournoi
        tournament_obj = create_tournament()

    else:
        print("Le tournoi doit être régénéré depuis la database.")
        views_input.wait_for_enter()
        return

    if tournament_obj is False:
        # impossible
        return

    if not isinstance(tournament_obj, Tournament):
        views_output.tournament_exist(tournament_obj)
        views_input.wait_for_enter
        return

    # print(tournament_obj)
    # save it on db >- No Add players before

    new_player = True
    while new_player is not False:
        views_utility.clear_screen
        views_output.players_list(ORDER_ALPHA)
        views_output.tournament_players(tournament_obj.get_id, ORDER_ALPHA)
        # Joueur pas dans la liste ?
        views_output.new_player()
        views_output.player_not_exist()
        response = views_input.y_or_n()
        if response is True:
            # create_player()
            players_controler()
        else:
            new_player = views_input.player_choice()
            if new_player is not False:
                print("Nouveau joueur_id: ", new_player)
                views_input.wait_for_enter()

        # verifier si déja ajouté
        # verifier si valide sur database
    # init
    # afficher le tournoi et sont status
    # nom date timeControl
    # roundsTerminés/nbrDeRounds
    # roundEnCours matchsRenseignés/matchsDuRound

    # ajouter des joueurs ! déja ajouté ?
    # afficher la liste des joueurs
    # demander quel joueur ajouter
    # afficher le menu input
    # le joueur est dans la liste -> le selectionner
    # le joueur n'est pas dans la liste -> le créer
    # afficher la liste des joueurs
    # tout les joueurs ont-il été ajoutés ?
    # verifier la quantité de joueurs et cloturer la création !!! irreverssible
    # mettre à jour le status du tournoi

    # initialiser un round ! quel round?
    # verifier le status du tournoi
    # verifier le status des rounds
    # verifier le nombre de rounds prévus
    # créer le round x
    # mettre à jour le status du round

    # créer les matchs ! quel round?
    # verifier le status des rounds
    # si round 1
    # appairer les joueurs par moitié
    # si non
    # appairer les joueurs suivant algo paires consecutives
    # afficher les matchs à jouer
    # mettre à jour le status du round

    # ... les joueurs jouent...

    # entrer le resultat d'un match ! quel round? quel match?
    # afficher les matchs du round en cours
    # input quel match renseigner ?
    # verifier si tous les matchs sont renseignés
    # afficher les matchs du round en cours
    # input demander cloturer le round

    # le round est-il terminé ?
    # le round est-il le dernier

    # le tournois est-il terminé ?


def create_tournament() -> Tournament | int:
    # afficher les tournois existants
    views_output.tournament_list()
    # input créer un tournoi ou quitter
    views_output.tournament_verify_before()
    response = views_input.y_or_n()
    if response is True:
        # input les datas pour la création
        tournament_dict = views_input.new_tournament()
        views_utility.clear_screen()
        views_output.tournament_data(tournament_dict)
        # changer le nombre de rounds ?
        views_output.adjust_round_quantity()
        response = views_input.y_or_n()
        new_round_quantity = ROUND_QUANTITY
        if response is True:
            new_round_quantity = views_input.change_round_quantity()
        # créer le tournoi
        tournament_obj = Tournament(
            tournament_dict["name"],
            tournament_dict["place"],
            tournament_dict["date"],
            tournament_dict["time_ctrl"],
            tournament_dict["description"],
        )
        if new_round_quantity != ROUND_QUANTITY:
            tournament_obj.set_round(new_round_quantity)
        # controler sur la database
        tournament_manager_obj = Db_manager_tournament()
        tournament_exist = tournament_manager_obj.add_one(tournament_obj)
        # verifier si déja existant
        if tournament_exist is not True:
            # return tournament_id
            return tournament_exist
        return tournament_obj
    return False

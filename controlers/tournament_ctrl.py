
from typing import List

from models.match import Match
from utils.constant import ORDER_ALPHA, PLAYER_QUANTITY_MIN, ROUND_QUANTITY
from views import views_input, views_menu, views_output, views_utility
from models.tournament import Tournament
from models.db_manager_tournaments import Db_manager_tournament
from models.db_manager_players import Db_manager_player
from controlers.players_controler import players_controler


def tournament_controler(tournament_id):
    """Controler for submenu tournament"""
    # tournoi non commencé   status = False
    #   le nombre de rounds est 0
    # tournoi cloturé    status = True
    #   le nombre de round à jouer est atteint
    #   tous les rounds sont cloturés

    # rounds en cours    valeur = 0 à max

    # round en cours     status = False
    #   la liste de matchs n'est pas cloturée
    # round cloturé      status = True
    #   la liste de matchs est cloturée

    # matchs en cours    status = False
    #   les matchs ne sont pas tous renseignés
    # matchs cloturé     status = True
    #   les matchs sont tous renseignés
    #   l'utilisateur a validé la cloture

    # tournament_id is False if choice = 7 > create tournament
    if tournament_id is False:
        # tournament init and save on database if not exist
        tournament_obj = create_tournament()

    # tournament_id is True if choice = 6 > rebuild tournament
    else:
        tournament_length = views_output.tournament_list()
        tournament_to_rebuild = views_input.tournament_choice(
            tournament_length)
        tournament_obj = rebuild_tournament(tournament_to_rebuild)

    if tournament_obj is False:
        # exit by user
        return

    # If tournament_obj = tournament_id on db
    if not isinstance(tournament_obj, Tournament):
        # tournament exist, go to previous menu
        views_output.tournament_exist(tournament_obj)
        views_input.wait_for_enter
        return

    # If no round in progress
    # It's possible to change round quantity and/or add player
    if len(tournament_obj.get_rounds) == 0:
        views_utility.clear_screen()
        views_output.tournament_data(tournament_obj)
        # Ask for changin number of rounds ?
        views_output.adjust_round_quantity()
        response = views_input.y_or_n()
        new_round_quantity = ROUND_QUANTITY
        if response is True:
            new_round_quantity = views_input.change_round_quantity()
        if new_round_quantity != ROUND_QUANTITY:
            tournament_obj.set_round(new_round_quantity)

        new_player = True
        while new_player is not False:
            views_utility.clear_screen
            players_id_list = views_output.players_list(ORDER_ALPHA)
            views_utility.crlf()
            views_output.tournament_players(tournament_obj.get_id, ORDER_ALPHA)
            players_quantity = len(tournament_obj.get_players)
            views_output.tournament_players_quantity(players_quantity)
            # Is player in list ?
            # Ask for create one
            views_output.player_not_exist()
            response = views_input.y_or_n()
            if response is True:
                # create player on database
                players_controler()
            else:
                views_output.new_player()
                new_player = views_input.player_choice()
                # Exit ?
                if new_player is not False:
                    # Check if player_id exist on db
                    if new_player in players_id_list:
                        # Add player on tournament and save players list on db
                        tournament_obj.add_player(new_player)
                        # Check if all players have a classification
                    else:
                        views_output.input_error()
        response = views_menu.tournament_begin()
        if response == 1:
            if players_quantity >= PLAYER_QUANTITY_MIN:
                play_tournament(tournament_obj)
            else:
                views_output.players_quantity_error(players_quantity)
                views_input.wait_for_enter()
    print("Fin provisoire")

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


def play_tournament(tournament_obj: Tournament):

    # le round 1 existe ?
    if len(tournament_obj.get_rounds) == 0:
        round_1 = create_round1(tournament_obj)
    else:
        round_1 = tournament_obj.get_rounds[0]

    # le round 1 est cloturé ?
    if not round_1.get_end:
        response = input_matchs_results(round_1)
        print("La reponse est: ", response)
    views_input.wait_for_enter()


def input_matchs_results(round):
    from models.round import Round
    round: Round = round
    response = ""
    while (response != "Q") and (response != "C"):
        match_obj_list = round.get_matchs
        views_utility.clear_screen()
        views_output.match_list(2, match_obj_list)
        response = views_input.match_choice()
        if (response != "Q") and (response != "C"):
            match_obj = match_obj_list[int(response)-1]
            views_utility.crlf()
            views_output.print_one_match(response, 2, match_obj)
            score_player_1 = views_input.match_results()
            score_player_2 = 1-score_player_1
            match_obj.set_score(score_player_1, score_player_2)
    return response


def create_round1(tournament_obj: Tournament):
    """Create round 1"""
    from models.player import Player
    from models.round import Round
    round_1 = Round("Round 1")
    player_manager_obj = Db_manager_player()
    # Build round1
    print("Création du round1")
    views_input.wait_for_enter()

    # create players_obj
    tournament_players_id_list = tournament_obj.get_players
    players_obj_list: list[Player] = []
    for player_id in tournament_players_id_list:
        player_obj = player_manager_obj.get_by_id(player_id)

        # player_obj: Player = create_player_obj(player_dict)

        players_obj_list.append(player_obj)
    print(players_obj_list)

    # Trie la liste de Player par leur classification, ascendant
    players_obj_list.sort(key=lambda x: x.get_player["classification"])
    # Sépare la liste en 2 listes
    list_1_length = len(players_obj_list)//2
    list_1 = players_obj_list[:list_1_length]
    list_2 = players_obj_list[list_1_length:]
    # Si le nombre de joueurs est impair,
    # le dernier ne peut-être apparié et reçois 1/2 point pour ne pas jouer
    if len(list_2) > len(list_1):
        tournament_obj.update_player_point(list_2[-1].get_id, 0.5)

    # Association des joueurs pour le round-1
    matches_list: List[tuple[Player, Player]] = []
    for i in range(len(list_1)):
        matches_list.append((list_1[i], list_2[i]))

    # Création de la listes des instances de Match pour le round_1
    round_x_matches_list: List[Match] = []

    print()
    print("Les match du premier tour sont:")

    for player_1, player_2 in matches_list:

        print(f"{player_1}\ncontre\n{player_2}\n")

        match = Match(player_1, player_2)
        round_x_matches_list.append(match)

    # Ajoute les Match dans le round_1
    for match in round_x_matches_list:
        round_1.add_match(match)
    return round_1


def rebuild_tournament(tournament_to_rebuild: int) -> Tournament:
    """Rebuild tournament from database"""
    tournament_obj = Tournament.add_tournament_from_db(tournament_to_rebuild)
    # print("Tournament after rebuild : ", tournament_obj)
    # views_input.wait_for_enter()
    return tournament_obj


def create_tournament() -> Tournament | int | bool:
    """Create a new tournament

    Return:
        Tournament | int | bool: tournament obj if succes, \
            tournament id if already exist, False if exit by user

    """
    tournament_manager_obj = Db_manager_tournament()
    views_output.tournament_list()
    # Ask for creating a new one
    views_output.tournament_verify_before()
    response = views_input.y_or_n()
    if response is True:
        tournament_dict = views_input.new_tournament()
        views_utility.clear_screen()
        tournament_obj = Tournament(
            tournament_dict["name"],
            tournament_dict["place"],
            tournament_dict["date"],
            tournament_dict["time_ctrl"],
            tournament_dict["description"],
        )
        views_output.tournament_data(tournament_obj)
        views_output.adjust_round_quantity()
        response = views_input.y_or_n()
        new_round_quantity = ROUND_QUANTITY
        if response is True:
            new_round_quantity = views_input.change_round_quantity()
        if new_round_quantity != ROUND_QUANTITY:
            tournament_obj.set_round(new_round_quantity)
        tournament_exist = tournament_manager_obj.add_one(tournament_obj)
        if tournament_exist is not True:
            # return tournament_id
            return tournament_exist
        return tournament_obj
    return response

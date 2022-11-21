
from typing import List

from models.match import Match
from utils.constant import (
    ORDER_ALPHA,
    PLAYER_QUANTITY_MIN,
    RESULT_MATCH,
    ROUND_QUANTITY
)
from views import views_input, views_output, views_utility
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

    if tournament_obj.get_status:
        # tournament is closed > Go to previous menu
        views_output.tournament_close()
        views_input.wait_for_enter()
        return

    # If no round in progress
    # It's possible to change round quantity and/or add player
    if len(tournament_obj.get_rounds) == 0:
        views_utility.clear_screen()
        views_output.tournament_data(tournament_obj)
        # Ask for changin number of rounds ?
        views_output.adjust_round_quantity()
        response = views_input.y_or_n()
        if response is True:
            new_round_quantity = views_input.change_round_quantity()
            if new_round_quantity != tournament_obj.get_round:
                tournament_obj.set_round(new_round_quantity)
                views_output.adjust_round_quantity()

        new_player = True
        while new_player is not False:
            views_utility.clear_screen
            players_id_list = views_output.players_list(ORDER_ALPHA)
            views_utility.crlf()
            views_output.tournament_players(tournament_obj, ORDER_ALPHA)
            players_quantity = len(tournament_obj.get_players)
            views_output.tournament_players_quantity(players_quantity)
            # Is player in list ?
            # Ask for create one
            new_player = views_input.add_player_on_tournament_choice()
            if new_player is True:
                # create player on database
                players_controler()
                # Go to while
                continue
            if new_player is False:
                # If new_player is False >>> End of while
                break
            # Check if player_id exist on db
            if new_player in players_id_list:
                # Add player on tournament and save players list on db
                tournament_obj.add_player(new_player)
            else:
                views_output.input_error()

    # Is PLAYER_QUANTITY_MIN Ok
    players_quantity = len(tournament_obj.get_players)
    if players_quantity < PLAYER_QUANTITY_MIN:
        views_output.players_quantity_error(players_quantity)
        views_input.wait_for_enter()
        # If not go to previous menu
        return

    # Check if all players have classification Ok
    # Ask if tournament ready to begin

    # Beguin or continue tournament
    # Round 1 exist ?
    if len(tournament_obj.get_rounds) < 1:
        # Create if not
        round_1 = create_round1(tournament_obj)
        tournament_obj.update_round(round_1)
    else:
        # Get it if yes
        round_1 = tournament_obj.get_rounds[0]

    # Round 1 is closed ?
    if not round_1.get_end:
        match_status = input_matchs_results(round_1, tournament_obj)
        if match_status:
            round_1.set_end
            # Info user for changing player classification before
            create_round_x(tournament_obj)
        if not round_1.get_end:
            # Round is not closed > go to previous menu
            return

    # For the next round not closed
    round_obj = find_next_round_to_complete(tournament_obj)
    # Is any round not closed
    if round_obj:
        ...
    else:
        # Ask for tournament close ?
        ...
        return

# verifier le status du tournoi
# verifier le status des rounds
# verifier le nombre de rounds prévus
# mettre à jour le status du round

# verifier le status des rounds
# afficher les matchs à jouer
# mettre à jour le status du round

# entrer le resultat d'un match ! quel round? quel match?
# afficher les matchs du round en cours
# input quel match renseigner ?
# verifier si tous les matchs sont renseignés
# afficher les matchs du round en cours
# input demander cloturer le round

# le round est-il terminé ?
# le round est-il le dernier

# le tournois est-il terminé ?

# le round 1 existe ?


def find_next_round_to_complete(tournament_obj: Tournament):
    """Find the first not closed round

    Args:
        tournament_obj (Tournament): current tournament

    Return:
        round_obj (Round): the first round not close in current tournament,
        or False if all rounds are closed

    """
    from models.round import Round
    round_obj_list: list[Round] = tournament_obj.get_rounds
    for round_obj in round_obj_list:
        if round_obj.get_end:
            return round_obj
    return False


def input_matchs_results(round, tournament_obj: Tournament) -> bool:
    """Update match's scores in round

    Arg:
        round (Round): round to update
        tournament_obj (Tournament): current tournament

    Return:
        bool: True if round must be closed, False if not

    """
    from models.round import Round
    round: Round = round
    response = ""
    while (response != "Q") and (response != "C"):
        match_obj_list = round.get_matchs
        views_utility.clear_screen()
        views_output.match_list(RESULT_MATCH, match_obj_list)
        response = views_input.match_choice()
        if (response != "Q") and (response != "C"):
            match_obj = match_obj_list[int(response)-1]
            views_utility.crlf()
            views_output.print_one_match(response, RESULT_MATCH, match_obj)
            player_1_id = match_obj.get_players[0].get_player["id"]
            player_2_id = match_obj.get_players[1].get_player["id"]
            score_player_1 = views_input.match_results()
            score_player_2 = 1-score_player_1
            match_obj.set_score(score_player_1, score_player_2)
            tournament_obj.update_player_point(player_1_id, score_player_1)
            tournament_obj.update_player_point(player_2_id, score_player_2)
            tournament_obj.update_round(round)

    round_status = False
    if response == "C":
        points_total = len(round.get_matchs)
        points_result = 0
        for match in round.get_matchs:
            score_player_1 = match.get_scores[0]
            score_player_2 = match.get_scores[1]
            if score_player_1:
                points_result += score_player_1
            if score_player_2:
                points_result += score_player_2
        if points_result == points_total:
            round_status = True
        else:
            views_output.round_not_complete()
            views_input.wait_for_enter()
    return round_status


def create_round1(tournament_obj: Tournament):
    """Create round 1"""
    from models.player import Player
    from models.round import Round
    round_1 = Round("Round 1")
    # Build round1
    print("Création du round1")
    views_input.wait_for_enter()

    # create players_obj
    players_obj_list = build_player_obj_list(tournament_obj)

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
    print("Affichage provisoire!!!\nLes match du premier tour sont:")

    for player_1, player_2 in matches_list:

        print(f"{player_1}\ncontre\n{player_2}\n")

        match = Match(player_1, player_2)
        round_x_matches_list.append(match)

    # Ajoute les Match dans le round_1
    for match in round_x_matches_list:
        round_1.add_match(match)
    return round_1


def build_player_obj_list(tournament_obj: Tournament):
    from models.player import Player
    player_manager_obj = Db_manager_player()
    tournament_players_id_list = tournament_obj.get_players
    players_obj_list: list[Player] = []
    for player_id in tournament_players_id_list:
        player_obj = player_manager_obj.get_by_id(player_id)
        players_obj_list.append(player_obj)
    return players_obj_list


def create_round_x(tournament_obj: Tournament):
    """Create round x

    Args:
        tournament_obj(Tournament): current tournament

    Return:
        round_x(Round): new round with matchs

    """
    rounds_in_tournament = len(tournament_obj.get_rounds)
    round_name = f"Round {rounds_in_tournament + 1}"
    from models.player import Player
    from models.round import Round
    round_x_obj = Round(round_name)
    # Build round x
    print(f"Création du round {round_name}")
    views_input.wait_for_enter()
    # create players_obj
    players_obj_list = build_player_obj_list(tournament_obj)

    # Create a list of forbiden pairs of player
    match_already_played = tournament_obj.get_matchs_already_played
    forbiden_pairs: List[tuple[Player, Player]] = []
    for match in match_already_played:
        pair = (match.get_players[0],
                match.get_players[1])
        forbiden_pairs.append(pair)

    # Create a list of free player to build the pairs
    # Free = True
    players_free = []
    for player_obj in players_obj_list:
        player_to_add = [player_obj, True]
        players_free.append(player_to_add)

    # Trie les joueurs par points puis par classement si égalité de points
    players_obj_list = sorted(
        players_obj_list,
        key=lambda x: x.get_player["classification"])
    players_obj_list = sorted(
        players_obj_list,
        key=lambda x: tournament_obj.get_points(x.get_id),
        reverse=True)

    print("Affichage provisoire\nJoueurs triés pour le prochain tour")
    for player_obj in players_obj_list:
        print(player_obj.get_player["name"],
              tournament_obj.get_points(player_obj.get_id),
              player_obj.get_player["classification"])

    matches_list = []
    rejected_players = []
    loop = 1

    while True:
        player_free = find_player_free(players_free)
        if loop <= 2:
            if loop == 1:
                # Find player 1 of the pair
                if player_free is None:
                    break
                player_1 = player_free
                loop = 2
            else:
                # Find player 2 of the pair
                if player_free is None:
                    # Player 1 is alone, give him 0.5 point
                    print(
                        f"Affichage provisoire\nLe joueur {player_1[0]} \
n'est pas associé, il faut lui donner 0.5 points")
                    player_obj: Player = player_1[0]
                    tournament_obj.update_player_point(player_obj.get_id, 0.5)
                    # Exit of while
                    break
                player_2 = player_free

                # Is this pair forbiden ?
                if (((player_1[0], player_2[0]) in forbiden_pairs)
                        or
                        ((player_2[0], player_1[0]) in forbiden_pairs)):

                    print(f"Affichage provisoire\nAlerte association \
interdite {player_1[0]} {player_2[0]}")

                    rejected_players.append(player_free)
                    free_flag = False
                    # Search for an otherfree player
                    for free_player in players_free:
                        if free_player[1] is True:
                            free_flag = True
                    # If yes make an other association
                    if free_flag is True:
                        # Retour au while
                        continue
                    # If no do association any way
                    print(
                        "Affichage provisoire\n\
Association contrainte *************************")
                    # Remove player_2 from rejected_players
                    rejected_players = [
                        rejected_player for rejected_player
                        in rejected_players
                        if rejected_player != player_2]
                # If succes, build match and add it to the list
                match = (player_1[0], player_2[0])
                matches_list.append(match)
                # In case of rejected player
                if len(rejected_players) > 0:
                    # Free the players in the list
                    for rejected_player in rejected_players:
                        index = players_free.index(rejected_player)
                        players_free[index][1] = True
                    # And empty the list
                    rejected_players = []
                # Ready for next loop
                loop = 1
                # print(match)
                # Go to while
    # Add created pairs to list of forbiden pairs
    forbiden_pairs.extend(matches_list)

    print()
    print(f"Affichage provisoire\n\
Les match du tour {round_x_obj.get_name} sont:")
    print()

    # Create Matchs and add them to the round x
    for player_1, player_2 in matches_list:

        print(f"Affichage provisoire\n{player_1}\ncontre\n{player_2}\n")

        match = Match(player_1, player_2)
        round_x_obj.add_match(match)

    # print(round_x_obj)
    # print()

    # Add round x to current tournament
    tournament_obj.update_round(round_x_obj)
    return round_x_obj


def find_player_free(players_free):
    """Find a free player

    Args:
        players_free(list[list[Player | bool]]):
        True > player is free to select False if not

    Return:
        Player | None: player free or None if no player is free

    """
    index = 0
    find = False
    while find is False and index < len(players_free):
        if players_free[index][1] is True:
            players_free[index][1] = False
            find = True
            return players_free[index]
        else:
            index += 1
    return None


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
        tournament_exist = tournament_manager_obj.add_one(tournament_obj)
        if tournament_exist is not True:
            # return tournament_id
            return tournament_exist
        return tournament_obj
    return response

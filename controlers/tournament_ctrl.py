
import time
from typing import List

from models.match import Match
from utils.constant import (
    ORDER_ALPHA,
    ORDER_CLASSIFICATION,
    PLAYER_ALONE_POINT,
    PLAYER_QUANTITY_MIN,
    RESULT_MATCH
)
from views import views_input, views_output, views_utility
from models.tournament import Tournament
from models.db_manager_tournaments import Db_manager_tournament
from models.db_manager_players import Db_manager_player
from controlers.players_controler import players_controler


def tournament_controler(start_menu_choice: bool):
    """Controler for submenu tournament

    Args:
        tournament_id(int): Tournament's id on database

    """

    # -----------------------------
    # Create or continue tournament
    # -----------------------------

    tournament_obj = create_or_rebuild_tournament(start_menu_choice)

    # Exit by user
    if tournament_obj is False:
        return

    # If tournament_obj == tournament_id on db
    if not isinstance(tournament_obj, Tournament):
        # tournament exist, go to previous menu
        views_output.tournament_exist(tournament_obj)
        views_input.wait_for_enter
        return

    # if tournament is closed > Go to previous menu
    if tournament_obj.get_status:
        views_output.tournament_close()
        views_input.wait_for_enter()
        return

    # If no round in progress
    # It's possible to change round quantity and/or add player
    if len(tournament_obj.get_rounds) == 0:
        response = prepare_tournament(tournament_obj)
        # Begin tournament ?
        if not response:
            # Go to previous menu
            return

    # Is PLAYER_QUANTITY_MIN Ok ?
    players_quantity = len(tournament_obj.get_players)
    if players_quantity < PLAYER_QUANTITY_MIN:
        views_output.players_quantity_error(players_quantity)
        views_input.wait_for_enter()
        # If not go to previous menu
        return

    # -----------------------------
    # Beguin or continue tournament
    # -----------------------------

    # Round 1 exist ?
    if len(tournament_obj.get_rounds) < 1:
        # Create it if not
        round_1_obj = create_round1(tournament_obj)
        tournament_obj.update_round(round_1_obj)
    else:
        # Get it if yes
        round_1_obj = tournament_obj.get_rounds[0]
    # Round 1 is closed ?
    if not round_1_obj.get_end:
        match_status = input_matchs_results(round_1_obj, tournament_obj)
        # if False > Exit
        if not match_status:
            # Go to previous menu
            return
        # if True > close round_1_obj
        round_1_obj.set_end(time.time())
        tournament_obj.update_round()

    # if round_1 closed
    while tournament_obj.get_status is False:
        # For the next round not closed
        round_x_obj = find_next_round_to_complete(tournament_obj)
        # If all rounds closed and tournament_round_quantity = ROUND_QUANTITY
        if ((
            round_x_obj is False
        ) and (
            len(tournament_obj.get_rounds) >= tournament_obj.get_round
        )):
            # Close tournament
            tournament_obj.set_status(True)
            views_output.tournament_end()
            views_input.wait_for_enter()
            # go to previous menu
            return

        # If all rounds closed, create a new one
        if round_x_obj is False:
            # Ask user to change player classification
            response = ask_classification_change(tournament_obj)
            if response:
                # Go to previous menu
                return
            round_x_obj = create_round_x(tournament_obj)

        match_status = input_matchs_results(round_x_obj, tournament_obj)
        # if False > Exit
        if not match_status:
            # Go to previous menu
            return
        # if True > close round_x
        round_x_obj.set_end(time.time())
        tournament_obj.update_round()
        if not round_x_obj.get_end:
            # Round_x is not closed > go to previous menu
            return


# --------------------------------
# Functions used in this controler
# --------------------------------


def ask_classification_change(tournament_obj: Tournament) -> bool:
    """Ask user for player classification change

    Args:
        Tournament: Current tournament

    Return:
        bool: True > User want to change, False if not

    """
    views_utility.clear_screen()
    views_utility.crlf()
    views_output.tournament_players(
        tournament_obj, ORDER_CLASSIFICATION)
    views_utility.crlf()
    views_output.player_change_classification()
    views_utility.crlf()
    response = views_input.y_or_n()
    return response


def prepare_tournament(tournament_obj: Tournament):
    """Prepare tournament before beguin

    Ask user for tournament data and round quantity, add players.

    Args:
        Tournament: Current tournament

    Return:
        bool: True > User want to beguin, False if not

    """
    views_utility.clear_screen()
    views_utility.crlf()
    views_output.tournament_data(tournament_obj)
    # Ask for changin number of rounds ?
    views_utility.crlf()
    views_output.adjust_round_quantity()
    views_utility.crlf()
    response = views_input.y_or_n()
    if response is True:
        views_utility.crlf()
        new_round_quantity = views_input.change_round_quantity()
        if new_round_quantity != tournament_obj.get_round:
            tournament_obj.set_round(new_round_quantity)
            views_output.adjust_round_quantity()
        # Chose players for current tournament
    response = add_player_in_tournament(tournament_obj)
    return response


def add_player_in_tournament(tournament_obj: Tournament):
    new_player = True
    while new_player is not False:
        views_utility.clear_screen()
        views_utility.crlf()
        # players_id_list of player on database
        players_id_list = views_output.players_list(ORDER_ALPHA)
        views_utility.crlf()
        views_output.tournament_players(tournament_obj, ORDER_ALPHA)
        players_quantity = len(tournament_obj.get_players)
        views_output.tournament_players_quantity(players_quantity)
        # Add a player:
        # int for player_id, True to create one, False to exit
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
            # Add player on tournament and save it on db
            tournament_obj.add_player(new_player)
        else:
            views_output.input_error()
    views_utility.clear_screen()
    views_output.tournament_data(tournament_obj)
    views_output.tournament_players(tournament_obj, ORDER_ALPHA)
    views_output.tournament_begin()
    response = views_input.y_or_n()
    return response


def create_or_rebuild_tournament(start_menu_choice: bool):
    """Create or rebuild tournament_obj

    Args:
        bool: False > Create, True > Rebuild

    Return:
        Tournament | int | bool: Tournament_obj if success in create or rebuild,
        Tournament_id if already exist, False if exit by user.

    """
    # start_menu_choice is False if choice = 7 > create tournament
    if start_menu_choice is False:
        # tournament init and save on database if not exist
        tournament_obj = create_tournament()

    # start_menu_choice is True if choice = 6 > rebuild tournament
    else:
        views_utility.clear_screen()
        views_utility.crlf()
        tournament_length = views_output.tournament_list()
        views_utility.crlf()
        tournament_to_rebuild = views_input.tournament_choice(
            tournament_length)
        tournament_obj = rebuild_tournament(tournament_to_rebuild)
    return tournament_obj


def find_next_round_to_complete(tournament_obj: Tournament) -> object | bool:
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
        if not round_obj.get_end:
            return round_obj
    return False


def input_matchs_results(round_obj, tournament_obj: Tournament) -> bool:
    """Update match's scores in current round

    Arg:
        round (Round): round to update
        tournament_obj (Tournament): current tournament

    Return:
        bool: True if round must be closed, False if not

    """
    from models.round import Round
    round_obj: Round = round_obj
    response = ""
    while (response != "Q") and (response != "C"):
        match_obj_list = round_obj.get_matchs
        views_utility.clear_screen()
        views_utility.crlf()
        views_output.current_round_matchs(round_obj.get_name)
        views_utility.crlf()
        views_output.match_list(RESULT_MATCH, match_obj_list)
        views_utility.crlf()
        response = views_input.match_choice()
        if (response != "Q") and (response != "C"):
            match_obj = match_obj_list[int(response) - 1]
            views_utility.crlf()
            views_output.print_one_match(response, RESULT_MATCH, match_obj)
            player_1_id = match_obj.get_players[0].get_player["id"]
            player_2_id = match_obj.get_players[1].get_player["id"]
            score_player_1 = views_input.match_results()
            score_player_2 = 1 - score_player_1
            match_obj.set_score(score_player_1, score_player_2)
            tournament_obj.update_player_point(player_1_id, score_player_1)
            tournament_obj.update_player_point(player_2_id, score_player_2)
            tournament_obj.update_round()

    round_status = False
    if response == "C":
        # Check if all match points are fill
        # With one point per match points_total must be == to points_result
        points_total = len(round_obj.get_matchs)
        points_result = 0
        for match in round_obj.get_matchs:
            score_player_1 = match.get_scores[0]
            score_player_2 = match.get_scores[1]
            # score could be None, 1.0, 0.5, or 0
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


def create_round1(tournament_obj: Tournament) -> object:
    """Create round 1

    Args:
        tournanment_obj(Tournament): Current tournament

    """
    from models.player import Player
    from models.round import Round
    round_1 = Round("Round 1")
    # Build round1
    # create players_obj
    players_obj_list = build_player_obj_list(tournament_obj)
    # Sort players by classification smallest first
    players_obj_list.sort(key=lambda x: x.get_player["classification"])
    # Cut in half
    list_1_length = len(players_obj_list) // 2
    list_1 = players_obj_list[:list_1_length]
    list_2 = players_obj_list[list_1_length:]
    # If number of player is odd,
    # the last one cant make a pair and get 0.5 point
    player_alone = False
    if len(list_2) > len(list_1):
        player_alone = list_2[-1]
        tournament_obj.update_player_point(
            player_alone.get_id, PLAYER_ALONE_POINT)
    # Make pairs for round-1
    matches_list: List[tuple[Player, Player]] = []
    for i in range(len(list_1)):
        matches_list.append((list_1[i], list_2[i]))
    # Build Matchs and add them to round
    for player_1, player_2 in matches_list:
        match = Match(player_1, player_2)
        round_1.add_match(match)
    # Display match list to play
    display_matchs_to_play(round_1, player_alone)
    return round_1


def display_matchs_to_play(round_obj, player_alone) -> None:
    """Display matchs to play in current round

    Args:
        round_obj(Round): Current round
        player_alone(Player | bool): Player if number \
            of player in tournament is odd, or False

    """
    from models.round import Round
    round_obj: Round = round_obj
    round_name = round_obj.get_name
    views_utility.clear_screen()
    views_utility.crlf()
    views_output.current_round_matchs(round_name)
    views_utility.crlf()
    views_output.match_list(RESULT_MATCH, round_obj.get_matchs)
    if player_alone:
        views_utility.crlf()
        views_output.player_alone(player_alone)
        views_utility.crlf()
    views_input.wait_for_enter()


def build_player_obj_list(tournament_obj: Tournament) -> list:
    """Build a list of Player

    Args:
        tournanment_obj(Tournament): Current tournament

    Return:
        list[Player]

    """
    from models.player import Player
    player_manager_obj = Db_manager_player()
    tournament_players_id_list = tournament_obj.get_players
    players_obj_list: list[Player] = []
    for player_id in tournament_players_id_list:
        player_obj = player_manager_obj.get_by_id(player_id)
        players_obj_list.append(player_obj)
    return players_obj_list


def create_round_x(tournament_obj: Tournament) -> object:
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

    players_obj_list = build_player_obj_list(tournament_obj)
    # Create a list of forbiden pairs of player
    match_already_played = tournament_obj.get_matchs_already_played
    forbiden_pairs: List[tuple[Player, Player]] = []
    for match in match_already_played:
        pair = (match.get_players[0], match.get_players[1])
        forbiden_pairs.append(pair)

    # Sort players by points and by classification in case of a tie
    players_obj_list = sorted(
        players_obj_list,
        key=lambda x: x.get_player["classification"])
    players_obj_list = sorted(
        players_obj_list,
        key=lambda x: tournament_obj.get_points(x.get_id),
        reverse=True)

    # Create a list of free player to build the pairs
    # True = Free
    players_free = []
    for player_obj in players_obj_list:
        player_to_add = [player_obj, True]
        players_free.append(player_to_add)

    matches_list = []
    rejected_players = []
    player_alone = False
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
                    # Player 1 is alone, give him PLAYER_ALONE_POINT point
                    player_alone: Player = player_1[0]
                    tournament_obj.update_player_point(
                        player_alone.get_id, PLAYER_ALONE_POINT)
                    # Exit of while
                    break
                player_2 = player_free

                # Is this pair forbiden ?
                if ((
                    (player_1[0], player_2[0]) in forbiden_pairs
                ) or (
                    (player_2[0], player_1[0]) in forbiden_pairs
                )):
                    # Forbiden pair {player_1[0]} {player_2[0]}
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
                    # Remove player_2 from rejected_players
                    rejected_players = [
                        rejected_player for rejected_player
                        in rejected_players
                        if rejected_player != player_2]
                # If successful, build match and add it to the list
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

    # Create Matchs and add them to the round x
    for player_1, player_2 in matches_list:
        match = Match(player_1, player_2)
        round_x_obj.add_match(match)
    # Add round x to current tournament
    tournament_obj.update_round(round_x_obj)
    display_matchs_to_play(round_x_obj, player_alone)
    return round_x_obj


def find_player_free(players_free: list) -> list | None:
    """Find a free player

    Args:
        players_free(list[list[Player | bool]]):
        True > player is free to select False if not

    Return:
        list | None: list[Player, bool] if bool is True, \
            or None if no player is free

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
    """Rebuild tournament from database

    Args:
        tournament_to_rebuild(int): id of the tournament

    """
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
    views_utility.clear_screen()
    views_utility.crlf()
    views_output.tournament_list()
    views_utility.crlf()
    # Ask for creating a new one
    views_output.tournament_verify_before()
    views_utility.crlf()
    response = views_input.y_or_n()
    if response is True:
        views_utility.clear_screen()
        views_utility.crlf()
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

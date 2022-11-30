from typing import Literal
import pyfiglet

from views import views_input, views_utility
from models.match import Match
from models.db_manager_players import Db_manager_player
from models.db_manager_tournaments import Db_manager_tournament
from utils.constant import (
    PLAYER_ALONE_POINT,
    PLAYER_NAME_LENGTH,
    PLAYER_QUANTITY_MIN,
    PLAYER_SURNAME_LENGTH,
    RESULT_MATCH,
    RESULT_ROUND,
    ROUND_QUANTITY,
    TOURNAMENT_DESCRIPTION_LENGTH,
    TOURNAMENT_NAME_LENGTH
)


def splash_screen():
    """Print splash screen"""
    views_utility.clear_screen()
    views_utility.crlf()
    text = pyfiglet.figlet_format("Bienvenue  au  tournoi  d' echecs")
    print(text)
    views_input.wait_for_enter()


def bye_screen():
    """Print bye screen"""
    views_utility.clear_screen()
    views_utility.crlf()
    text = pyfiglet.figlet_format("Au revoir")
    print(text)
    print("Merci d'avoir utilisé ce programme.")


def players_list(sort_type: Literal[1, 2]) -> list[int]:
    """Build player list sorted by sort_type and call print_player()

    Args:
        Literal[1, 2]: ORDER_ALPHA, ORDER_CLASSIFICATION

    Return:
        list[int]: players's id

    """
    manager_player_obj = Db_manager_player()
    players_obj_list = manager_player_obj.get_all()
    player_dict_list: list[dict] = []
    players_id: list[int] = []
    for player_obj in players_obj_list:
        player_dict = player_obj.get_player
        player_dict_list.append(player_dict)
        players_id.append(player_dict["id"])
    sorted_players = views_utility.sort_players_by_type(
        sort_type, player_dict_list)
    print("Liste des joueurs sur la base de données")
    print()
    print_players(sorted_players)
    return players_id


def print_players(sorted_players: list[dict]):
    """Print sorted list of players

    Args:
        list[dict]: list sorted of player's dict

    """
    for sorted_player in sorted_players:
        id = sorted_player['id']
        name = sorted_player['name']
        surname = sorted_player['surname']
        gender = sorted_player['gender']
        birth_date = sorted_player['birth_date']
        classification = sorted_player['classification']

        print('{0:>3}  {1:{name_length}}  {2:{surname_length}}  \
{3:{gender_length}}  né le: {4:{Date_length}}  classé:{5:>{class_length}}'
              .format(
                  id,
                  name,
                  surname,
                  gender,
                  birth_date,
                  classification,
                  name_length=PLAYER_NAME_LENGTH,
                  surname_length=PLAYER_SURNAME_LENGTH,
                  gender_length=1,
                  Date_length=10,
                  class_length=6
              ))


def print_player(player):
    """Print a player

    Args:
        Player: player obj to print

    """
    from models.player import Player
    player_obj: Player = player
    player_dict = player_obj.get_player

    id = player_dict['id']
    name = player_dict['name']
    surname = player_dict['surname']
    gender = player_dict['gender']
    birth_date = player_dict['birth_date']
    classification = player_dict['classification']

    print('{0:>3}  {1:{name_length}}  {2:{surname_length}}  \
{3:{gender_length}}  né le:{4:{Date_length}}  classé:{5:>{class_length}}'
          .format(
              id,
              name,
              surname,
              gender,
              birth_date,
              classification,
              name_length=PLAYER_NAME_LENGTH,
              surname_length=PLAYER_SURNAME_LENGTH,
              gender_length=1,
              Date_length=10,
              class_length=6
          ))


def player_exist(player_id):
    """Print info <player exist on db>"""
    print(f"Ce joueur est déja enregistré sous le numéro: {player_id}")


def player_alone(player):
    from models.player import Player
    player_obj: Player = player
    print(f"Le joueur {player_obj.get_player['name']} \
{player_obj.get_player['surname']} n'as pas trouvé d'adverssaire et \
reçoit {PLAYER_ALONE_POINT} points")


def player_change_classification():
    print("Vous allez débuter un nouveau round.")
    print("Souhaitez-vous allez dans le menu joueur pour \
changer un classement.")


def player_sort_type() -> None:
    print("Pour la liste des joueurs")


def player_result(tournament):
    from models.tournament import Tournament
    tournament_obj: Tournament = tournament
    manager_player_obj = Db_manager_player()
    # Dict with player_id in key and points for the tournament in value
    tournament_players_dict = tournament_obj.get_players
    # Make a copy
    round_player_dict = dict(tournament_players_dict)
    # And set all points to 0
    for key in round_player_dict:
        round_player_dict[key] = 0

    views_utility.clear_screen()
    print()
    print(f'Classement des joueurs pour {tournament_obj.get_name}')
    print()
    sorted_player_obj_list = sort_player_dict(
        manager_player_obj, tournament_players_dict)
    print_sorted_result(sorted_player_obj_list)
    # for each round in round list
    for round in tournament_obj.get_rounds:
        # if round is closed
        if round.get_end:
            # for each match in round
            for match in round.get_matchs:
                player_1_id = match.get_players[0].get_id
                player_2_id = match.get_players[1].get_id
                player_1_points = match.get_scores[0]
                player_2_points = match.get_scores[1]
                round_player_dict[str(player_1_id)] = player_1_points
                round_player_dict[str(player_2_id)] = player_2_points
            # Begin sorted list
            sorted_player_obj_list = sort_player_dict(
                manager_player_obj, round_player_dict)
            # Display round results
            print()
            print(f"Classement des joueurs pour le {round.get_name}")
            print()
            print_sorted_result(sorted_player_obj_list)


def print_sorted_result(sorted_player_obj_list):
    for classement, item in enumerate(sorted_player_obj_list, 1):
        print("{0:>3}: {1:{name_length}} {2:{surname_length}} \
classé:{3:6}   avec {4:>2} {5:}".format(
            classement,
            item[0].get_player["name"],
            item[0].get_player["surname"],
            item[0].get_player["classification"],
            item[1],
            "point" if item[1] < 2 else "points",
            name_length=PLAYER_NAME_LENGTH,
            surname_length=PLAYER_SURNAME_LENGTH
        ))


def sort_player_dict(manager_player_obj, player_dict):
    tuple_list = []
    # Build a list of tupple(player_id, points)
    for key in player_dict.keys():
        tuple_list.append((int(key), player_dict[key]))
        # Build a sorted list by player classification
    sorted_list = sorted(
        tuple_list,
        key=lambda key:
        (manager_player_obj.get_by_id(key[0]).get_classification)
    )
    # Sort by points
    sorted_list = sorted(
        sorted_list,
        key=lambda x: x[1],
        reverse=True
    )
    # Build a new list with player_obj in place of player_id
    sorted_player_obj_list = []
    for item in sorted_list:
        sorted_player_obj_list.append(
            (manager_player_obj.get_by_id(item[0]), item[1]))

    return sorted_player_obj_list


def tournament_list() -> int:
    """Print tournament list from db

    Return:
        int: length of the list
    """
    tournament_manager_obj = Db_manager_tournament()
    tournaments_obj_list = tournament_manager_obj.get_all()
    print("Liste des tournois sur la base de données")
    print()
    for tournament_obj in tournaments_obj_list:
        tournament_dict = tournament_obj.get_tournament
        id = tournament_dict["id"]
        name = tournament_dict["name"]
        date = tournament_dict["date"]
        description = tournament_dict["description"]
        time_ctrl = tournament_dict["time_ctrl"]
        tournament_big_obj = tournament_manager_obj.get_one_from_db(id)
        status = "Erreur"
        player_quantity = -1
        if tournament_big_obj:
            player_quantity = len(tournament_big_obj.get_players)
            status = ("En cours" if tournament_dict["status"] is False
                      else "Cloturé")
        print('{0:>3} {1:{name_length}}  {2:10}  \
{3:{description_length}}  {4:8}  {5:6}  {6:>3} joueurs'.format(
            id,
            name,
            date,
            description,
            status,
            time_ctrl,
            player_quantity,
            name_length=TOURNAMENT_NAME_LENGTH,
            description_length=TOURNAMENT_DESCRIPTION_LENGTH
        ))
    return len(tournaments_obj_list)


def tournament_data(tournament):
    """Print a tournament

    Args:
        Tournament: tournament_obj

    """
    from models.tournament import Tournament
    tournament_obj: Tournament = tournament
    tournament_dict = tournament_obj.get_tournament
    print(
        f'Le tournoi "{tournament_dict["name"]}" se déroule le \
{tournament_dict["date"]} à {tournament_dict["place"]}.')
    print(
        f'Le controle du temps est "{tournament_dict["time_ctrl"]}" \
et il est prévu {ROUND_QUANTITY} rounds.')
    print(tournament_dict["description"])


def tournament_results(tournament_id: int, result_type):
    """Print tournament's results by result_type

    Args:
        int: tournament's id
        Literal[1, 2]: tournament's rounds = 1, tournament's matchs = 2

    """
    manager_tournament_obj = Db_manager_tournament()
    rounds_obj_list = manager_tournament_obj.get_rounds_by_tournament_id(
        tournament_id)
    round_txt = "Les rounds du tournoi"
    match_txt = "Les matchs du tournoi"
    print(f'{ round_txt if result_type == RESULT_ROUND else match_txt}')
    for round_obj in rounds_obj_list:
        print()
        if result_type == RESULT_ROUND:
            round_status = ("En cours" if round_obj.get_end is False
                            else "Cloturé")
            print(round_obj.get_name, round_status)
        match_obj_list = round_obj.get_matchs
        match_list(result_type, match_obj_list)


def tournament_end():
    print("Ce tournoi est maintenant terminé.")


def match_list(result_type, match_obj_list):
    for index, match_obj in enumerate(match_obj_list, 1):
        print_one_match(index, result_type, match_obj)


def print_one_match(index: int, result_type, match_obj):
    match_dict = make_match_dict(match_obj)
    player1_name = match_dict["player_1_name"]
    player1_surname = match_dict["player_1_surname"]
    space1 = ""
    for i in range(PLAYER_NAME_LENGTH - len(player1_name)):
        space1 += " "
    space2 = ""
    for i in range(PLAYER_SURNAME_LENGTH - len(player1_surname)):
        space2 += " "

    player2_name = match_dict["player_2_name"]
    player2_surname = match_dict["player_2_surname"]
    space3 = ""
    for i in range(PLAYER_NAME_LENGTH - len(player2_name)):
        space3 += " "
    space4 = ""
    for i in range(PLAYER_SURNAME_LENGTH - len(player2_surname)):
        space4 += " "

    tab = "\t" if result_type == RESULT_ROUND else ""
    index_str = "  " + str(index)
    match_number = f"{index_str[-3:]}: " if result_type == RESULT_MATCH else ""
    score_player_1 = ("" if match_dict["score_player_1"]
                      is None else match_dict["score_player_1"])
    score_player_2 = ("" if match_dict["score_player_2"]
                      is None else match_dict["score_player_2"])

    print(f'{tab}{match_number}\
{player1_name}{space1} {player1_surname}{space2}\
contre   {player2_name}{space3} {player2_surname}{space4} \
score: {score_player_1} / {score_player_2}')


def make_match_dict(match_obj: Match):
    player1 = match_obj.get_players[0]
    player2 = match_obj.get_players[1]
    match_dict = {
        "player_1_name": player1.get_player["name"],
        "player_1_surname": player1.get_player["surname"],
        "player_2_name": player2.get_player["name"],
        "player_2_surname": player2.get_player["surname"],
        "score_player_1": match_obj.get_match[0][1],
        "score_player_2": match_obj.get_match[1][1]
    }
    return match_dict


def tournament_players(tournament, sort_type):
    from models.tournament import Tournament
    tournament_obj: Tournament = tournament
    """Build player list sorted by sort_type and call print_player()

    Args:
        tournament(Tournament): current tournament
        Literal[1, 2]: ORDER_ALPHA, ORDER_CLASSIFICATION

    """

    manager_player = Db_manager_player()
    tournament_players_id = tournament_obj.get_players
    players: list[dict] = []
    for tournament_player_id in tournament_players_id:
        player_obj = manager_player.get_by_id(tournament_player_id)
        if player_obj:
            player_dict = player_obj.get_player
            players.append(player_dict)
    sorted_players = views_utility.sort_players_by_type(sort_type, players)
    print("Liste des joueurs du tournoi")
    print()
    print_players(sorted_players)


def tournament_players_quantity(players_quantity):
    """Print info number of player

    Args:
        int: player quantity
    """
    print(
        f'\nVous avez actuellement {players_quantity} \
{"joueurs ajoutés" if players_quantity > 1 else "joueur ajouté"} au tournoi.')


def tournament_verify_before():
    """Print CTA <verify before create a new tournament>"""
    print("Veuillez vérifier que le tournoi n'existe pas dèja")
    print("Créer un nouveau ?")


def tournament_exist(tournament_id):
    """Print info <tournament exist on db>"""
    print(f"Ce tournoi est déja enregistré sous le numéro: {tournament_id}")


def tournament_close():
    print("Ce tournoi est clos, il n'est pas possible de le modifier")


def tournament_begin():
    print("Une fois le tournoi commencé, il ne sera plus possible de :")
    print("\t- changer le nombre de round")
    print("\t- ajouter des joueurs")
    print()
    print("Voulez-vous débuter le tournoi ?")


def adjust_round_quantity():
    """Ask user for changing number of round"""
    print("Souhaitez-vous changer le nombre de round?")


def round_not_complete():
    print("Les scores doivent être entièrement \
renseignés avant de cloturer le round")


def current_round_matchs(round_name):
    print(f"Les matchs du {round_name} sont:")


def players_quantity_error(players_quantity):
    """Print info PLAYER_QUANTITY_MIN

    Args:
        int: players quantity in tournament

    """
    print(f"Vous avez entré {players_quantity} joueurs pour le tournoi")
    print(f"La quantité minimum est {PLAYER_QUANTITY_MIN}")


def input_error():
    """Print info <input error>"""
    print("Erreur de saisie")


def forbiden_delete():
    """Print info <forbiden delete>"""
    print("Ne peut pas être modifié ou supprimé")


def confirm_delete():
    """Ask user for player permanent delete"""
    print("Voulez-vous définitivement supprimer ce joueur ?")

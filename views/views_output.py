from typing import Literal
import pyfiglet

from views import views_utility
from models.match import Match
from models.db_manager_players import Db_manager_player
from models.db_manager_tournaments import Db_manager_tournament
from utils.constant import (
    PLAYER_NAME_LENGTH,
    PLAYER_QUANTITY_MIN,
    PLAYER_SURNAME_LENGTH,
    RESULT_MATCH,
    RESULT_ROUND,
    ROUND_QUANTITY
)


def splash_screen():
    """Print splash screen"""
    views_utility.clear_screen()
    text = pyfiglet.figlet_format("Bienvenue  au  tournoi  d' echecs")
    print(text)
    print("Entrée pour continuer")
    input()


def bye_screen():
    """Print bye screen"""
    views_utility.clear_screen()
    text = pyfiglet.figlet_format("Au revoir")
    print(text)
    print("Merci d'avoir utilisé ce programme.\nEntrée pour quitter")
    input()


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
    print_players(sorted_players)
    return players_id


def print_players(sorted_players: list[dict]):
    """Print sorted list of player

    Args:
        list[dict]: list sorted of player's dict

    """
    for sorted_player in sorted_players:
        print(f"{sorted_player['id']} {sorted_player['name']} \
{sorted_player['surname']} {sorted_player['gender']} né le: \
{sorted_player['birth_date']} classé: {sorted_player['classification']}")


def print_player(player_obj):
    """Print a player

    Args:
        Player: player obj to print

    """
    from models.player import Player
    player_obj: Player = player_obj
    player_dict = player_obj.get_player
    print(f"{player_dict['id']} {player_dict['name']} \
{player_dict['surname']} {player_dict['gender']} né le: \
{player_dict['birth_date']}")


def player_exist(player_id):
    """Print info <player exist on db>"""
    print(f"Ce joueur est déja enregistré sous le numéro: {player_id}")


def tournament_list() -> int:
    """Print tournament list from db

    Return:
        int: length of the list >
            must be change in futur by a list of tournaments_id

    """
    tournament_bd = Db_manager_tournament()
    tournaments_obj_list = tournament_bd.get_all()
    views_utility.clear_screen()
    for tournament_obj in tournaments_obj_list:
        tournament_dict = tournament_obj.get_tournament
        print(tournament_dict["id"], tournament_dict["name"],
              tournament_dict["date"], tournament_dict["description"])
    return len(tournaments_obj_list)


def tournament_data(tournament_obj):
    """Print a tournament

    Args:
        Tournament: tournament_obj

    """
    from models.tournament import Tournament
    tournament_obj: Tournament = tournament_obj
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
    tournament_db = Db_manager_tournament()
    rounds_obj_list = tournament_db.get_rounds_by_tournament_id(tournament_id)
    # print(rounds)
    for round_obj in rounds_obj_list:
        if result_type == RESULT_ROUND:
            print(round_obj.get_name)
        match_obj_list = round_obj.get_matchs
        match_list(result_type, match_obj_list)


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
    if result_type == RESULT_ROUND:
        print()


def make_match_dict(match_obj: Match):
    player1 = match_obj.get_match[0][0]
    player2 = match_obj.get_match[1][0]
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
    tournament: Tournament = tournament
    """Build player list sorted by sort_type and call print_player()

    Args:
        tournament(Tournament): current tournament
        Literal[1, 2]: ORDER_ALPHA, ORDER_CLASSIFICATION

    """

    manager_player = Db_manager_player()
    tournament_players_id = tournament.get_players
    players: list[dict] = []
    for tournament_player_id in tournament_players_id:
        player_obj = manager_player.get_by_id(tournament_player_id)
        player_dict = player_obj.get_player
        players.append(player_dict)
    sorted_players = views_utility.sort_players_by_type(sort_type, players)
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


def adjust_round_quantity():
    """Ask user for changing number of round"""
    print("Souhaitez-vous changer le nombre de round?")


def round_not_complete():
    print("Les scores doivent être entièrement \
renseignés avant de cloturer le round")


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
    print("Voulez-vous definitivement supprimer ce joueur ?")

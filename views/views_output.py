import pyfiglet

from views import views_utility
from models.db_manager_players import Db_manager_player
from models.db_manager_tournaments import Db_manager_tournament
from utils.constant import (
    PLAYER_NAME_LENGTH,
    PLAYER_QUANTITY_MIN,
    PLAYER_SURNAME_LENGTH,
    ROUND_QUANTITY)


def splash_screen():
    views_utility.clear_screen()

    text = pyfiglet.figlet_format("Bienvenue  au  tournoi  d' echecs")
    print(text)
    print("Entrée pour continuer")
    input()


def bye_screen():
    views_utility.clear_screen()
    text = pyfiglet.figlet_format("Au revoir")
    print(text)
    print("Merci d'avoir utilisé ce programme.\nEntrée pour quitter")
    input()


def players_list(sort_type) -> list:
    db_player = Db_manager_player()
    players_document = db_player.get_all()
    players = []
    players_id = []
    for player_document in players_document:
        player = views_utility.build_players_dict(player_document)
        players.append(player)
        players_id.append(player["id"])
    sorted_players = views_utility.sort_players_by_type(sort_type, players)
    print_players(sorted_players)
    return players_id


def print_players(sorted_players):
    for sorted_player in sorted_players:
        print(f"{sorted_player['id']} {sorted_player['name']} \
{sorted_player['surname']} {sorted_player['gender']} né le: \
{sorted_player['birth_date']} classé: {sorted_player['classification']}")


def print_player(player):
    print(f"{player.doc_id} {player['name']} \
{player['surname']} {player['gender']} né le: \
{player['birth_date']}")


def player_exist(player_id):
    print(f"Ce joueur est déja enregistré sous le numéro: {player_id}")


def new_player():
    print("Entrer le numéro du joueur à ajouter au tournoi.")


def player_not_exist():
    print("Le joueur à ajouter n'est pas dans la liste! \
Voulez-vous l'ajouter? ", end="")


def tournament_list() -> int:
    tournament_bd = Db_manager_tournament()
    tournaments_list = tournament_bd.get_all()
    views_utility.clear_screen()
    for tournament in tournaments_list:
        print(tournament["id"], tournament["name"],
              tournament["date"], tournament["description"])
    return len(tournaments_list)


def tournament_data(tournament_obj):
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
    tournament_db = Db_manager_tournament()
    rounds = tournament_db.get_rounds_by_id(tournament_id)
    # print(rounds)
    for round in rounds:
        if result_type == 1:
            print(round["name"])
        matchs = round["matchs"]
        for match in matchs:
            player1 = match["player_1"]
            space1 = ""
            for i in range(PLAYER_NAME_LENGTH - len(player1["name"])):
                space1 += " "
            space2 = ""
            for i in range(PLAYER_SURNAME_LENGTH - len(player1["surname"])):
                space2 += " "
            player2 = match["player_2"]
            space3 = ""
            for i in range(PLAYER_NAME_LENGTH - len(player2["name"])):
                space3 += " "
            space4 = ""
            for i in range(PLAYER_SURNAME_LENGTH - len(player2["surname"])):
                space4 += " "
            tab = "\t" if result_type == 1 else ""
            print(f'{tab}\
{player1["name"]}{space1} {player1["surname"]}{space2}\
contre   {player2["name"]}{space3} {player2["surname"]}{space4} \
score: {match["score_player_1"]} / {match["score_player_2"]}')
        if result_type == 1:
            print()


def tournament_players(tournament_id: int, sort_type: int):
    db_player = Db_manager_player()
    db_tournament = Db_manager_tournament()
    tournament_players = db_tournament.get_players_by_id(tournament_id)
    players = []
    for tournament_player in tournament_players:
        player_document = db_player.get_by_id(int(tournament_player))
        player = views_utility.build_players_dict(player_document)
        players.append(player)
    sorted_players = views_utility.sort_players_by_type(sort_type, players)
    print_players(sorted_players)


def tournament_players_quantity(players_quantity):
    print(
        f'\nVous avez actuellement {players_quantity} \
{"joueurs ajoutés" if players_quantity > 1 else "joueur ajouté"} au tournoi.')


def tournament_verify_before():
    print("Veuillez vérifier que le tournoi n'existe pas dèja")
    print("Créer un nouveau ?")


def tournament_exist(tournament_id):
    print(f"Ce tournoi est déja enregistré sous le numéro: {tournament_id}")


def adjust_round_quantity():
    print("Souhaitez-vous changer le nombre de round?")


def players_quantity_error(players_quantity):
    print(f"Vous avez entré {players_quantity} joueurs pour le tournoi")
    print(f"La quantité minimum est {PLAYER_QUANTITY_MIN}")


def input_error():
    print("Erreur de saisie")


def forbiden_delete():
    print("Ne peut pas être modifié ou supprimé")


def confirm_delete():
    print("Voulez-vous definitivement supprimer ce joueur ?")

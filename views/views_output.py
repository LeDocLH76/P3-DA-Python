import pyfiglet

from views import views_utility
from models.db_manager_players import Db_manager_player
from models.db_manager_tournaments import Db_manager_tournament
from utility.constant import ROUND_QUANTITY


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


def players_list(sort_type):
    db_player = Db_manager_player()
    players_document = db_player.get_all()
    players = []
    for player_document in players_document:
        player = views_utility.build_players_list(player_document)
        players.append(player)
    sorted_players = views_utility.sort_players_by_type(sort_type, players)
    print_players(sorted_players)


def print_players(sorted_players):
    views_utility.clear_screen()
    for sorted_player in sorted_players:
        print(f"{sorted_player['id']} {sorted_player['name']} \
{sorted_player['surname']} {sorted_player['gender']} né le: \
{sorted_player['birth_date']} classé: {sorted_player['classification']}")


def print_player(player):
    print(f"{player.doc_id} {player['name']} \
{player['surname']} {player['gender']} né le: \
{player['birth_date']}")


def tournament_list():
    tournament_bd = Db_manager_tournament()
    tournaments_list = tournament_bd.get_all()
    views_utility.clear_screen()
    for tournament in tournaments_list:
        print(tournament["id"], tournament["name"],
              tournament["date"], tournament["description"])
    return len(tournaments_list)


def tournament_data(tournament_dict):
    print(
        f'Le tournoi "{tournament_dict["name"]}" se déroule le {tournament_dict["date"]} à \
{tournament_dict["place"]}.')
    print(
        f'Le controle du temps est "{tournament_dict["time_ctrl"]}" et il est prévu {ROUND_QUANTITY} rounds.')
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
            for i in range(20 - len(player1["name"])):
                space1 += " "
            space2 = ""
            for i in range(20 - len(player1["surname"])):
                space2 += " "
            player2 = match["player_2"]
            space3 = ""
            for i in range(20 - len(player2["name"])):
                space3 += " "
            space4 = ""
            for i in range(20 - len(player2["surname"])):
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
        player = views_utility.build_players_list(player_document)
        players.append(player)
    sorted_players = views_utility.sort_players_by_type(sort_type, players)
    print_players(sorted_players)


def player_exist(player_id):
    print(f"Ce joueur est déja enregistré sous le numéro: {player_id}")


def input_error():
    print("Erreur de saisie")


def forbiden_delete():
    print("Ne peut pas être modifié ou supprimé")


def confirm_delete():
    print("Voulez-vous definitivement supprimer ce joueur ?")

import pyfiglet
from operator import itemgetter
from tinydb import TinyDB

from views import views_utility


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


def tournament_list():
    db = TinyDB('chess_tournament')
    tournaments_table = db.table("tournaments")
    views_utility.clear_screen()
    for document in tournaments_table:
        print(document.doc_id, document["name"],
              document["date"], document["description"])
    return tournaments_table.__len__()


def players_list(sort_type):
    db = TinyDB('chess_tournament')
    players_table = db.table("players")
    players_document = players_table.all()
    players = []
    for player_document in players_document:
        player = build_players_list(player_document)
        players.append(player)
    sorted_players = sort_players_by_type(sort_type, players)
    print_players(sorted_players)


def print_players(sorted_players):
    views_utility.clear_screen()
    for sorted_player in sorted_players:
        print(f"{sorted_player['name']} {sorted_player['surname']} \
{sorted_player['gender']} né le: {sorted_player['birth_date']} classé: \
{sorted_player['classification']}")


def sort_players_by_type(sort_type, players):
    if sort_type == 1:
        sorted_players = sorted(players, key=itemgetter('name', 'surname'))
    else:
        sorted_players = sorted(players, key=itemgetter(
            'classification', 'name', 'surname'))
    return sorted_players


def build_players_list(player_document):
    player = {}
    player["name"] = player_document["name"]
    player["surname"] = player_document["surname"]
    player["gender"] = player_document["gender"]
    player["birth_date"] = views_utility.transform_date(
        player_document["birth_date"])
    player["classification"] = player_document["classification"]
    return player


def tournament_results(tournament_id, result_type):
    db = TinyDB('chess_tournament')
    tournaments_table = db.table("tournaments")
    tournament = tournaments_table.get(doc_id=tournament_id)
    rounds = tournament.get("rounds")
    # print(rounds)
    for round in rounds:
        if result_type == 1:
            print(round["name"])
        matchs = round.get("matchs")
        for match in matchs:
            player1 = match.get("player_1")
            space1 = ""
            for i in range(20 - len(player1["name"])):
                space1 += " "
            space2 = ""
            for i in range(20 - len(player1["surname"])):
                space2 += " "
            player2 = match.get("player_2")
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


def tournament_players(tournament_id, sort_type):
    db = TinyDB('chess_tournament')
    tournaments_table = db.table("tournaments")
    players_table = db.table("players")
    tournament = tournaments_table.get(doc_id=tournament_id)
    tournament_players = tournament.get('players')
    players = []
    for tournament_player in tournament_players:
        player_document = players_table.get(doc_id=int(tournament_player))
        player = build_players_list(player_document)
        players.append(player)
    sorted_players = sort_players_by_type(sort_type, players)
    print_players(sorted_players)

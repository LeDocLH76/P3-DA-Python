from tinydb import TinyDB, where
from models.match import Match
from models.player import Player
from models.round import Round

from models.tournament import Tournament

db = TinyDB('chess_tournament')
tournament_to_rebuild = "Tournoi privé"
# regénération du tournoi
tournaments_table = db.table("tournament")
tournament_db = tournaments_table.get(where("name") == tournament_to_rebuild)
# print(tournament_db["name"])
# print(tournament_db["place"])
# print(tournament_db["date"])
# print(tournament_db["round"])
# print(tournament_db["time_ctrl"])
# print(tournament_db["description"])
tournament = Tournament(
    tournament_db["name"],
    tournament_db["place"],
    tournament_db["date"],
    tournament_db["time_ctrl"],
    tournament_db["description"],
    tournament_db["round"])

# print(tournament)

# regénération des joueurs
players_table = db.table("players")
for player_db in players_table:
    # print(player_db["name"])
    # print(player_db["surname"])
    # print(player_db["birth_date"])
    # print(player_db["gender"])
    # print(player_db["classification"])
    # print(player_db["points"])
    birth_date: str = (player_db["birth_date"])
    birth_date_fr = "/".join(reversed(birth_date.split("-")))
    player = Player(
        player_db["name"],
        player_db["surname"],
        birth_date_fr,
        player_db["gender"],
        player_db["classification"])
    tournament.add_player(player)
    player.add_point(player_db["points"])

# regénération des tournées et rounds
players_obj = tournament.get_players
for index, round_db in enumerate(tournament_db["rounds"]):
    round_name = round_db["name"]
    round = Round(round_name)
    # regénération des matchs
    for match_db in round_db["matchs"]:
        # Recherche l'instance du joueur 1 dans la liste
        player_1 = [
            player for player in players_obj
            if (player.get_player["name"]
                == match_db["player_1"]["name"])
            and (player.get_player["surname"]
                 == match_db["player_1"]["surname"])
            and (player.get_player["birth_date"]
                 == match_db["player_1"]["birth_date"])]
        score_player_1 = match_db["score_player_1"]
        player_1 = player_1[0]
        # Recherche l'instance du joueur 2 dans la liste
        player_2 = [
            player for player in players_obj
            if (player.get_player["name"]
                == match_db["player_2"]["name"])
            and (player.get_player["surname"]
                 == match_db["player_2"]["surname"])
            and (player.get_player["birth_date"]
                 == match_db["player_2"]["birth_date"])]
        score_player_2 = match_db["score_player_2"]
        player_2 = player_2[0]

        match = Match(player_1, player_2, score_player_1, score_player_2)
        round.add_match(match)
    tournament.add_round(round)


print(tournament)
for round_item in tournament.get_round:
    print(f"Le round {round_item.get_name} est composé des matchs:")
    for match in round_item.get_matchs:
        print(f"{match.get_match[0][0]} contre {match.get_match[1][0]} \
score: {match.get_match[0][1]}/{match.get_match[1][1]}")

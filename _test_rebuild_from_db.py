from tinydb import TinyDB
from models.player import Player
from models.match import Match
from models.round import Round
from models.tournament import Tournament

db = TinyDB('chess_tournament')
tournament_to_rebuild = 2

# regénération du tournoi
tournaments_table = db.table("tournaments")
tournament_db = tournaments_table.get(doc_id=tournament_to_rebuild)
tournament: Tournament = Tournament.add_tournament_from_db(
    tournament_db["name"],
    tournament_db["place"],
    tournament_db["date"],
    tournament_db["time_ctrl"],
    tournament_db["description"],
    tournament_db["players"],
    tournament_db["round"],
)

# regénération des joueurs
players_obj = []
tournament_players_db = tournament_db["players"]
players_table = db.table("players")
# Crée la liste des key des joueurs
players_id = [key for key in tournament_players_db]
# Crée la liste des points des joueurs
points = [tournament_players_db[key] for key in tournament_players_db]
# Pour chaque key dans tournament_players_db
for player_id, points in zip(players_id, points):
    # Recupère les datas du joueur doc_id = key dans la table players
    player_info = players_table.get(doc_id=player_id)
# Crée le player
    player_obj: Player = Player.add_player_from_db(
        player_info["name"],
        player_info["surname"],
        player_info["birth_date"],
        player_info["gender"],
        player_info["classification"],
        player_id)
# L'ajoute au tournoi avec ses points
    tournament.update_player_point_from_db(player_id, points)
# Ajoute l'instance de ce joueur à la liste pour ce tournoi
    players_obj.append(player_obj)

# regénération des tournées et rounds
rounds = []
for round_item in tournament_db["rounds"]:
    round_name = round_item["name"]
    round_obj = Round(round_name)
    # regénération des matchs
    for match_db in round_item["matchs"]:
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
        round_obj.add_match(match)
    rounds.append(round_obj)
tournament.add_rounds_from_bd(rounds)

print(tournament)
for round_item in tournament.get_rounds:
    print(f"Le round {round_item.get_name} est composé des matchs:")
    for match in round_item.get_matchs:
        print(f"{match.get_match[0][0]} contre {match.get_match[1][0]} \
score: {match.get_match[0][1]}/{match.get_match[1][1]}")

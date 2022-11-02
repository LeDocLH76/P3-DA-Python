from typing import List
from models.player import Player
from models.match import Match
from models.round import Round
from models.tournament import Tournament
from models.db_manager_tournaments import Db_manager_tournament
from models.db_manager_players import Db_manager_player

tournament_to_rebuild = 1

# regénération du tournoi
manager_tournament_obj = Db_manager_tournament()
tournament_db = manager_tournament_obj.get_one(tournament_to_rebuild)
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
manager_player_obj = Db_manager_player()
players_obj = []
tournament_players_db = manager_tournament_obj.get_players_by_id(
    tournament_to_rebuild)
# Crée la liste des key des joueurs
players_id = [key for key in tournament_players_db]
# Crée la liste des points des joueurs
points = [tournament_players_db[key] for key in tournament_players_db]
# Pour chaque key dans tournament_players_db
for player_id, points in zip(players_id, points):
    # Recupère les datas du joueur
    player_info = manager_player_obj.get_by_id(player_id)
    # Crée le player
    player_obj_to_add: Player = Player.add_player_from_db(
        player_info["name"],
        player_info["surname"],
        player_info["birth_date"],
        player_info["gender"],
        player_info["classification"],
        player_id)
    # L'ajoute au tournoi avec ses points
    tournament._players[str(player_id)] = points
    # Ajoute l'instance de ce joueur à la liste pour ce tournoi
    players_obj.append(player_obj_to_add)

# regénération des tournées et matchs
rounds_list = []
rounds_db_list = manager_tournament_obj.get_rounds_by_id(tournament_to_rebuild)
for round_item in rounds_db_list:
    # Teste si le match est clos
    if round_item["date_end"] is not None:
        round_obj_to_add = Round.add_round_from_db(
            round_item["name"],
            round_item["date_begin"],
            round_item["date_end"]
        )
    else:
        # Round is not close
        round_obj_to_add = Round.add_round_from_db(
            round_item["name"],
            round_item["date_begin"]
        )

    # regénération des matchs du round
    for match_db in round_item["matchs"]:
        # Recherche l'instance du joueur 1 dans la liste
        players_obj: List[Player]
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
        round_obj_to_add.add_match(match)
    rounds_list.append(round_obj_to_add)
tournament._rounds = rounds_list

print(tournament)
print()
print("Voici les infos du tournoi:")
for round_item in tournament.get_rounds:
    print(f"Le round {round_item.get_name}")
    print(f"Début :{round_item.get_begin}")
    print(f"fin :{round_item.get_end}")
    print("Il est composé des matchs:")
    for match in round_item.get_matchs:
        print(f"{match.get_match[0][0]} contre {match.get_match[1][0]} \
score: {match.get_match[0][1]}/{match.get_match[1][1]}")
    print()

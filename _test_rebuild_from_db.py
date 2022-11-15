from models.db_manager_tournaments import Db_manager_tournament
# from models.tournament import Tournament

tournament_to_rebuild = 1

# La regénération du tournoi est maintenat éffectuée dans le manager
manager_tournament_obj = Db_manager_tournament()
tournament = manager_tournament_obj.get_one_from_db(tournament_to_rebuild)
# tournament = Tournament.add_tournament_from_db_2(tournament_to_rebuild)

print(tournament)
print()
print("Voici les infos du tournoi:")
for round_item in tournament.get_rounds:
    print(f"Le round {round_item.get_name}")
    print(f"Début :{round_item.get_begin}")
    print(f"Fin :{round_item.get_end}")
    print("Il est composé des matchs:")
    for match in round_item.get_matchs:
        print(f"{match.get_match[0][0]} contre {match.get_match[1][0]} \
score: {match.get_match[0][1]}/{match.get_match[1][1]}")
    print()


from models.tournament import Tournament


tournament_to_rebuild = 1
tournament = Tournament.add_tournament_from_db_2(tournament_to_rebuild)

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

players_list: list[dict] = [{1: 41}, {2: 42}, {3: 43}, {4: 44}]
for player_dict in players_list:
    player_id = list(player_dict.keys())[0]
    points = list(player_dict.values())[0]
    print(f"player_id = {player_id} points = {points}")
# Voir db_manager_tournament get_one()
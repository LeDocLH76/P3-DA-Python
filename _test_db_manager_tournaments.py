from tinydb import TinyDB


db = TinyDB('chess_tournament')
tournaments_table = db.table("tournaments")
tournament = tournaments_table.get(doc_id=1)
rounds_list = tournament.get('rounds')

for round in rounds_list:
    print(round["name"])
    for match in round["matchs"]:
        print(match["player_1"]["name"])
        print(match["player_1"]["surname"])
        print(match["player_1"]["birth_date"])
        print(match["player_1"]["gender"])
        print(match["player_1"]["classification"])
        print(match["score_player_1"])
        print(match["player_2"]["name"])
        print(match["player_2"]["surname"])
        print(match["player_2"]["birth_date"])
        print(match["player_2"]["gender"])
        print(match["player_2"]["classification"])
        print(match["score_player_2"])

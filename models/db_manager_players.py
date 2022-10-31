from tinydb import Query, TinyDB, where


class Db_manager_player:
    def __init__(self):
        db = TinyDB('chess_tournament')
        self.players_table = db.table("players")

    def get_all(self):
        return self.players_table.all()

    def get_by_id(self, player_id: int):
        return self.players_table.get(doc_id=player_id)

    def update_classification_by_id(self, player_id, classification):
        self.players_table.update(
            {"classification": classification}, doc_ids=[player_id])

    def add_one(self, player_dict):
        player = Query()
        if not self.players_table.search(
            (player.name == player_dict["name"])
            & (player.surname == player_dict["surname"])
                & (player.birth_date == player_dict["birth_date"])):
            player_id = self.players_table.insert(player_dict)
        else:
            print("Cet enregistrement est déja présent en base!")
            # Find player_id on Db, put it in self
            player_db = self.players_table.get(
                (where("name") == player_dict["name"])
                & (where("surname") == player_dict["surname"])
                & (where("birth_date") == player_dict["birth_date"]))
            player_id = player_db.doc_id
        print(f"Id du joueur ={player_id}")
        return player_id

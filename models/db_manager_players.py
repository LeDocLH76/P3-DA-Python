from tinydb import Query, TinyDB, where


class Db_manager_player:
    def __init__(self):
        db = TinyDB('chess_tournament')
        self.players_table = db.table("players")

    def get_all(self):
        return self.players_table.all()

    def get_by_id(self, player_id: int):
        return self.players_table.get(doc_id=player_id)

    def update_by_id(self, player_id, player_dict):
        list_to_update = [player_id]
        list_player_updated = self.players_table.update(
            player_dict, doc_ids=list_to_update)
        return list_player_updated

    def update_classification_by_id(self, player_id, classification):
        self.players_table.update(
            {"classification": classification}, doc_ids=[player_id])

    def add_one(self, player_dict):
        player = Query()
        if not self.players_table.search(
            (player.name == player_dict["name"])
            & (player.surname == player_dict["surname"])
                & (player.birth_date == player_dict["birth_date"])):
            # Create player in db and get id
            player_id = self.players_table.insert(player_dict)
        else:
            player_id = self.get_id(player_dict)
        return player_id

    def delete_one(self, player_id):
        list_to_remove = [player_id]
        list_player_removed = self.players_table.remove(doc_ids=list_to_remove)
        return list_player_removed

    def get_id(self, player_dict):
        player_db = self.players_table.get(
            (where("name") == player_dict["name"])
            & (where("surname") == player_dict["surname"])
            & (where("birth_date") == player_dict["birth_date"]))
        return player_db.doc_id

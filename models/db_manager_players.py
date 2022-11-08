from tinydb import Query, TinyDB


class Db_manager_player:
    def __init__(self):
        db = TinyDB('chess_tournament')
        self.players_table = db.table("players")

    def get_all(self):
        self.players_table.clear_cache()
        return self.players_table.all()

    def get_by_id(self, player_id: int):
        return self.players_table.get(doc_id=player_id)

    def add_one(self, player_obj, player_id: int | None = None) -> int:
        from models.player import Player
        player_obj: Player = player_obj
        player_dict = player_obj.get_player
        # update player
        if player_id is not None:
            list_to_update = [player_id]
            self.players_table.update(
                player_dict, doc_ids=list_to_update)
            return player_id
        # add player
        player = Query()
        # player exist ?
        if not self.players_table.search(
            (player.name == player_dict["name"])
            & (player.surname == player_dict["surname"])
                & (player.birth_date == player_dict["birth_date"])):
            # Create player in db and get id
            player_id = self.players_table.insert(player_dict)
            player_obj.set_id(player_id)
        else:
            player_id = player_obj.get_id
        return player_id

    def delete_one(self, player_id):
        list_to_remove = [player_id]
        list_player_removed = self.players_table.remove(doc_ids=list_to_remove)
        return list_player_removed

    def update_classification_by_id(self, player_id, classification):
        self.players_table.update(
            {"classification": classification}, doc_ids=[player_id])

from tinydb import Query, TinyDB


class Db_manager_player:
    def __init__(self):
        db = TinyDB('chess_tournament')
        self.players_table = db.table("players")

    def get_all(self):
        from models.player import Player
        self.players_table.clear_cache()
        players_document_list = self.players_table.all()
        player_obj_list: list[Player] = []
        for player_document in players_document_list:
            player = Player.add_player_from_db(
                player_document['name'],
                player_document["surname"],
                player_document["birth_date"],
                player_document["gender"],
                player_document["classification"],
                player_document.doc_id
            )
            player_obj_list.append(player)
        return player_obj_list

    def get_by_id(self, player_id: int):
        from models.player import Player
        player_document = self.players_table.get(doc_id=player_id)
        if player_document is not None:
            player_obj = Player.add_player_from_db(
                player_document['name'],
                player_document["surname"],
                player_document["birth_date"],
                player_document["gender"],
                player_document["classification"],
                player_document.doc_id
            )
            return player_obj
        return None

    def add_one(self, player_obj, player_id: int | None = None) -> bool | int:
        from models.player import Player
        player_obj: Player = player_obj
        player_dict = player_obj.get_player
        # update player
        if player_id is not None:
            list_to_update = [player_id]
            self.players_table.update(
                player_dict, doc_ids=list_to_update)
            return True
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
            return True
        else:
            # Player already exist, find is id and return it
            player_db = self.players_table.get(
                (player.name == player_dict["name"])
                & (player.surname == player_dict["surname"])
                & (player.birth_date == player_dict["birth_date"]))
            player_id = player_db.doc_id
        return player_id

    def delete_one(self, player_id):
        list_to_remove = [player_id]
        list_player_removed = self.players_table.remove(doc_ids=list_to_remove)
        return list_player_removed

    def update_classification_by_id(self, player_id, classification):
        self.players_table.update(
            {"classification": classification}, doc_ids=[player_id])

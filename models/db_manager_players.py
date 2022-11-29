from tinydb import Query, TinyDB


class Db_manager_player:
    """Manager for player table on database"""

    def __init__(self):
        db = TinyDB('chess_tournament')
        self.players_table = db.table("players")

    def get_all(self):
        """Get all player on db

        Return:
            list[Player]: list of player obj

        """

        from models.player import Player
        self.players_table.clear_cache()
        players_document_list = self.players_table.all()
        player_obj_list: list[Player] = []
        for player_document in players_document_list:
            player_obj = self._make_player(player_document)
            player_obj_list.append(player_obj)
        return player_obj_list

    def _make_player(self, player_document):
        """Make a player obj

        Args:
            Document: player from db

        Return:
            Player: player obj

        """

        from models.player import Player
        player = Player.add_player_from_db(
            player_document['name'],
            player_document["surname"],
            player_document["birth_date"],
            player_document["gender"],
            player_document["classification"],
            player_document.doc_id
        )
        return player

    def get_by_id(self, player_id: int):
        """Get one player on db

        Return:
            Player: player obj if id exist on db, None if not

        """

        player_document = self.players_table.get(doc_id=player_id)
        if player_document is not None:
            player_obj = self._make_player(player_document)
            return player_obj
        return None

    def add_one(self, player, player_id: int | None = None) -> bool | int:
        """Add or update a player on db

        Args:
            Player: player to add or update
            int: player id: if present update it, else create it

        Return:
            bool | int: True in succes for update or create,
                        player id if create an existing one

        """

        from models.player import Player
        player_obj: Player = player
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
        if not self.players_table.search((
            player.name == player_dict["name"]
        ) & (
            player.surname == player_dict["surname"]
        ) & (
            player.birth_date == player_dict["birth_date"]
        )):
            # Create player in db and get id
            player_id = self.players_table.insert(player_dict)
            player_obj.set_id(player_id)
            return True
        else:
            # Player already exist, find and return is id
            player_db = self.players_table.get((
                player.name == player_dict["name"]
            ) & (
                player.surname == player_dict["surname"]
            ) & (
                player.birth_date == player_dict["birth_date"]
            ))
            if player_db:
                player_id = player_db.doc_id
                return player_id
        # This never append
        return False

    def delete_one(self, player_id):
        """Delete a player on db

        Args:
            int: player id to delete

        Return:
            int: player id removed on db

        """
        list_to_remove = [player_id]
        list_player_removed = self.players_table.remove(doc_ids=list_to_remove)
        player_removed_id = list_player_removed[0]
        return player_removed_id

    def update_classification_by_id(self, player_id, classification):
        """Update classification of one player

        Args:
            int: player id
            int: new classification

        """

        self.players_table.update(
            {"classification": classification}, doc_ids=[player_id])

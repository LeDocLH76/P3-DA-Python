from tinydb import Query, TinyDB

from models.match import Match
from models.round import Round
from models.db_manager_players import Db_manager_player
from utils.transform_date import date_iso2fr


class Db_manager_tournament:
    """Manager for tournament table on database"""

    def __init__(self):
        db = TinyDB('chess_tournament')
        self.tournaments_table = db.table("tournaments")

    def get_all(self):
        """Get all tournament on db only base info

        Return:
            list[Tournament]: list of tournament obj

        """
        from models.tournament import Tournament
        tournaments_obj_list: list[Tournament] = []
        for document in self.tournaments_table:
            tournament_id = document.doc_id
            tournament_obj = self.get_one(tournament_id)
            tournaments_obj_list.append(tournament_obj)
        return tournaments_obj_list

    def get_one(self, tournament_id):
        """Get one tournament on db only base info

        Args:
            int: tournament id

        Return:
            Tournament: tournament obj

        """

        from models.tournament import Tournament
        document = self.tournaments_table.get(doc_id=tournament_id)
        tournament_obj = Tournament(
            document["name"],
            document["place"],
            document["date"],
            document["time_ctrl"],
            document["description"],
            document["round"]
        )
        tournament_obj.set_id(document.doc_id)
        tournament_obj.set_status(document["status"])
        return tournament_obj

    def _get_players_by_tournament_id(self, tournament_id: int) -> dict:
        """Get players of one tournament

        Args:
            int: tournament id

        Return:
            dict: key = id of player, value = points of the player

        """
        tournament_obj = self.tournaments_table.get(doc_id=tournament_id)
        player_dict: dict = tournament_obj.get('players')
        return player_dict

    def get_players_all_tournaments(self) -> set[int]:
        """Get players of all tournaments

        Return:
            set[int]: id of players

        """

        tournaments_obj_list = self.get_all()
        players_set: set[int] = set()
        for tournament_obj in tournaments_obj_list:
            players_dict = self._get_players_by_tournament_id(
                tournament_obj.get_id)
            player_id_list = [int(key) for key in players_dict]
            players_set.update(player_id_list)
        return players_set

    def get_one_from_db(self, tournament_id: int):
        """Get complete obj tournament from db

        Args:
            int: tournament id

        Return:
            Tournament: base info + players + rounds + matchs
        """
        tournament_obj = self.get_one(tournament_id)
        document_tournament = self.tournaments_table.get(doc_id=tournament_id)
        # Create Players list
        self._create_players_obj_list(tournament_id)
        tournament_players_dict = document_tournament["players"]
        # Extract players_id from key
        players_id: list[int] = [key for key in tournament_players_dict]
        # Extract player_ point with key
        players_points: list[int] = [
            tournament_players_dict[key] for key in tournament_players_dict
        ]
        for player_id, player_points in zip(players_id, players_points):
            tournament_obj.add_player_from_db(player_id, player_points)
        # Create rounds and matchs
        round_obj_list = self.get_rounds_by_tournament_id(tournament_id)
        for round_obj in round_obj_list:
            tournament_obj.add_round_from_db(round_obj)
        return tournament_obj

    def get_rounds_by_tournament_id(self, tournament_id: int) -> list[Round]:
        """Get rounds of a tournament

        Args:
            int: tournament id

        Return:
            list[Round]: list of round obj with matchs

        """
        document_tournament = self.tournaments_table.get(doc_id=tournament_id)
        rounds_db_list = document_tournament["rounds"]
        players_obj_list = self._create_players_obj_list(tournament_id)
        round_obj_list: list[Round] = []
        for round_item in rounds_db_list:
            # Create one round
            # Round is close ?
            if round_item["date_end"] is not None:
                round_obj = Round.add_round_from_db(
                    round_item["name"],
                    round_item["date_begin"],
                    round_item["date_end"]
                )
            else:
                # Round is not close
                round_obj = Round.add_round_from_db(
                    round_item["name"],
                    round_item["date_begin"]
                )
            # Create matchs
            for match_db in round_item["matchs"]:
                birth_date_iso_player_1 = match_db["player_1"]["birth_date"]
                birth_date_iso_player_2 = match_db["player_2"]["birth_date"]
                birth_date_fr_player_1 = date_iso2fr(birth_date_iso_player_1)
                birth_date_fr_player_2 = date_iso2fr(birth_date_iso_player_2)
                match_db["player_1"]["birth_date"] = birth_date_fr_player_1
                match_db["player_2"]["birth_date"] = birth_date_fr_player_2
                # Find player1 in list
                player_1 = [
                    player for player in players_obj_list
                    if ((
                        player.get_player["name"]
                    ) == (
                        match_db["player_1"]["name"]
                    )
                    ) and ((
                        player.get_player["surname"]
                    ) == (
                        match_db["player_1"]["surname"]
                    )
                    ) and ((
                        player.get_player["birth_date"]
                    ) == (
                        match_db["player_1"]["birth_date"]
                    ))]
                score_player_1 = match_db["score_player_1"]
                player_1 = player_1[0]
                # Find player2 in list
                player_2 = [
                    player for player in players_obj_list
                    if ((
                        player.get_player["name"]
                    ) == (
                        match_db["player_2"]["name"]
                    )
                    ) and ((
                        player.get_player["surname"]
                    ) == (
                        match_db["player_2"]["surname"]
                    )
                    ) and ((
                        player.get_player["birth_date"]
                    ) == (
                        match_db["player_2"]["birth_date"]
                    ))]
                score_player_2 = match_db["score_player_2"]
                player_2 = player_2[0]
                # Create one match
                match_obj = Match(player_1,
                                  player_2,
                                  score_player_1,
                                  score_player_2
                                  )
                round_obj.add_match(match_obj)
            round_obj_list.append(round_obj)
        return round_obj_list

    def update_players_by_tournament_id(self, tournament_obj):
        """Update players dict of one tournament on db

        Args:
            str: name of tournament
            str: date of tournament
            dict: key = id of player, value = points of the player

        """

        from models.tournament import Tournament
        tournament_obj: Tournament = tournament_obj
        tournament_id = tournament_obj.get_id
        tournament_players = tournament_obj.get_players
        self.tournaments_table.update(
            {"players": tournament_players}, doc_ids=[tournament_id])

    def update_round_quantity_by_tournament_id(self, tournament_obj):
        """Update round quantity  by tournament id

        Args:
            tournament_obj(Tournament): Current tournament

        """
        from models.tournament import Tournament
        tournament_obj: Tournament = tournament_obj
        tournament_id = tournament_obj.get_id
        tournament_round_quantity = tournament_obj.get_round
        self.tournaments_table.update(
            {"round": tournament_round_quantity}, doc_ids=[tournament_id])

    def update_status_by_tournament_id(self, tournament_obj):
        """Update tournament status  by tournament id

        Args:
            tournament_obj(Tournament): Current tournament

        """
        from models.tournament import Tournament
        tournament_obj: Tournament = tournament_obj
        tournament_id = tournament_obj.get_id
        tournament_status = tournament_obj.get_status
        self.tournaments_table.update(
            {"status": tournament_status}, doc_ids=[tournament_id])

    def add_one(self, tournament_obj) -> bool | int:
        """Add a tournament base info on db

        Args:
            Tournament: tournament obj

        Return:
            bool | int: True if succes, tournament id if already exist

        """

        from models.tournament import Tournament
        tournament_obj: Tournament = tournament_obj
        tournament_dict = tournament_obj.get_tournament
        tournament = Query()
        # tournament exist ?
        if not self.tournaments_table.search(
                (
                    tournament.name == tournament_dict["name"]
                ) & (
                    tournament.date == tournament_dict["date"]
                )):
            # Create tournament in db and get id
            tournament_id = self.tournaments_table.insert(tournament_dict)
            tournament_obj.set_id(tournament_id)
            return True
        else:
            # Tournament already exist, find is id and return it
            tournament_db = self.tournaments_table.get(
                (
                    tournament.name == tournament_dict["name"]
                ) & (
                    tournament.date == tournament_dict["date"]
                )
            )
            tournament_id = tournament_db.doc_id
        return tournament_id

    def update_rounds_by_tournament_id(self, tournament_obj):
        """Update rounds of one tournament on db

        Args:
            str: name of tournament
            str: date of tournament
            list[Round]: list of round obj to update

        """
        from models.tournament import Tournament
        tournament_obj: Tournament = tournament_obj
        tournament_id = tournament_obj.get_id
        tournament_rounds = tournament_obj.get_rounds

        # Build rounds infos
        rounds_list = []
        for round in tournament_rounds:
            round_to_add = {"name": round.get_name}
            round_to_add["date_begin"] = round.get_begin
            round_to_add["date_end"] = round.get_end
            # Build matchs infos
            matchs = []
            for match in round.get_matchs:
                match_to_add = {
                    "player_1": match.get_players[0].get_player,
                    "player_2": match.get_players[1].get_player,
                    "score_player_1": match.get_scores[0],
                    "score_player_2": match.get_scores[1]}
                matchs.append(match_to_add)
            round_to_add.update({"matchs": matchs})
            rounds_list.append(round_to_add)

        # Update database
        self.tournaments_table.update(
            {"rounds": rounds_list}, doc_ids=[tournament_id])

    def _create_players_obj_list(self, tournament_id):
        """Create a list of player obj of a tournament

        Args:
            int: tournament id

        Return:
            list[Player]: list of player obj

        """
        from models.player import Player
        manager_player_obj = Db_manager_player()
        players_obj_list: list[Player] = []
        document_tournament = self.tournaments_table.get(doc_id=tournament_id)
        tournament_players_dict = document_tournament["players"]
        # Extract players_id from key
        players_id: list[int] = [key for key in tournament_players_dict]
        for player_id in players_id:
            # Find data of one player
            player_obj = manager_player_obj.get_by_id(player_id)
            player_dict = player_obj.get_player
            # Create one player
            player_obj_to_add: Player = Player.add_player_from_db(
                player_dict["name"],
                player_dict["surname"],
                player_dict["birth_date"],
                player_dict["gender"],
                player_dict["classification"],
                player_id)
            # Add Player to Players for this tournament
            players_obj_list.append(player_obj_to_add)
        return players_obj_list

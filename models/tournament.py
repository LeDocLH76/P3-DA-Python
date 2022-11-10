from typing import List
from models.db_manager_players import Db_manager_player

from models.match import Match
from models.player import Player
from models.round import Round
from models.db_manager_tournaments import Db_manager_tournament


class Tournament:
    def __init__(self, name, place, date, time_ctrl, description, round=4):
        """Tournament definition

        Attributes:
            name (str): Tournament's name
            place (srt): Tournament's place
            date (str): Tournament's date
            round (int): Number of round for the tournament
            time_ctrl (str): Bullet, blitz, rapid, only one of them
            description (str): General description
            rounds (list): List of Round object
            players (dict): Key = player's id on database, \
                value = player's points for this tournament
            id (int): Tournament's id on the database

        """
        self._name: str = name
        self._place: str = place
        self.set_date(date)
        self._round: int = round
        self._time_ctrl: str = time_ctrl
        self._description: str = description
        self._rounds: List[Round] = []
        self._players = {}
        self._status = False

    @classmethod
    def add_tournament_from_db(cls,
                               name,
                               place,
                               date,
                               time_ctrl,
                               description,
                               players,
                               id,
                               round=4):
        """Alternative __init__ to create Tournament from database

        Args:
            name (str): Tournament's name
            place (srt): Tournament's place
            date (str): Tournament's date
            time_ctrl (str): Bullet, blitz, rapid, only one of them
            description (str): General description
            players (dict): Key = player's id on database, \
                value = player's points for this tounament
            round (int): Number of round for the tournament

        """
        tournament = cls.__new__(cls)
        tournament._name = name
        tournament._place = place
        tournament._date = date
        tournament._time_ctrl = time_ctrl
        tournament._description = description
        tournament._players = players
        tournament._id = id
        tournament._round = round
        return tournament

    @classmethod
    def add_tournament_from_db_2(cls, tournament_id: int):
        """Alternative __init__ to create Tournament from database

        Args:
            tournament_id (int): Tournament's id to rebuild

        Return:
            object: Tournament
        """

        manager_tournament_obj = Db_manager_tournament()
        tournament_db = manager_tournament_obj.get_one(tournament_id)
        # Create tournament
        tournament = cls.__new__(cls)
        tournament._name = tournament_db["name"]
        tournament._place = tournament_db["place"]
        tournament._date = tournament_db["date"]
        tournament._time_ctrl = tournament_db["time_ctrl"]
        tournament._description = tournament_db["description"]
        tournament._players = tournament_db["players"]
        tournament._id = tournament_id
        tournament._round = tournament_db["round"]

        # Create tournament's players
        manager_player_obj = Db_manager_player()
        players_obj = []
        tournament_players_db = manager_tournament_obj.get_players_by_id(
            tournament_id)
        # Extract players_id from key
        players_id = [key for key in tournament_players_db]
        # Extract points from value
        points = [tournament_players_db[key] for key in tournament_players_db]
        for player_id, points in zip(players_id, points):
            # Find data of one player
            player_info = manager_player_obj.get_by_id(player_id)
            # Create one player
            player_obj_to_add: Player = Player.add_player_from_db(
                player_info["name"],
                player_info["surname"],
                player_info["birth_date"],
                player_info["gender"],
                player_info["classification"],
                player_id)
            # Add one player to list of players in tournament with is points
            tournament._players[str(player_id)] = points
            # Add player to players for this tournament
            players_obj.append(player_obj_to_add)

        # Create rounds and matchs
        rounds_list = []
        rounds_db_list = manager_tournament_obj.get_rounds_by_id(tournament_id)
        for round_item in rounds_db_list:
            # Create one round
            # Round is close ?
            if round_item["date_end"] is not None:
                round_obj_to_add = Round.add_round_from_db(
                    round_item["name"],
                    round_item["date_begin"],
                    round_item["date_end"]
                )
            else:
                # Round is not close
                round_obj_to_add = Round.add_round_from_db(
                    round_item["name"],
                    round_item["date_begin"]
                )
            # Create matchs
            for match_db in round_item["matchs"]:
                # Find player1 in list
                players_obj: List[Player]
                player_1 = [
                    player for player in players_obj
                    if (player.get_player["name"]
                        == match_db["player_1"]["name"])
                    and (player.get_player["surname"]
                         == match_db["player_1"]["surname"])
                    and (player.get_player["birth_date"]
                         == match_db["player_1"]["birth_date"])]
                score_player_1 = match_db["score_player_1"]
                player_1 = player_1[0]
                # Find player2 in list
                player_2 = [
                    player for player in players_obj
                    if (player.get_player["name"]
                        == match_db["player_2"]["name"])
                    and (player.get_player["surname"]
                         == match_db["player_2"]["surname"])
                    and (player.get_player["birth_date"]
                         == match_db["player_2"]["birth_date"])]
                score_player_2 = match_db["score_player_2"]
                player_2 = player_2[0]
                # Create one match
                match = Match(player_1, player_2,
                              score_player_1, score_player_2)
                # Add one match to the list
                round_obj_to_add.add_match(match)
            # Add one round to the list
            rounds_list.append(round_obj_to_add)
        tournament._rounds = rounds_list
        return tournament

    def set_date(self, date: str) -> None:
        """Set tournament's date

        Args:
            date (str): Date for this tournament

        """
        self._date = date

    def set_status(self, new_status: bool) -> None:
        self._status = new_status

    def set_round(self, new_round_quantity) -> None:
        self._round = new_round_quantity

    def set_id(self, tournament_id) -> None:
        self._id = tournament_id

    def update_round(self, round: Round = None) -> None:
        """Add a round in the list and update rounds in database

        Args:
            round (Round): If not None, add the round

        """
        if round is not None:
            self._rounds.append(round)
        rounds = []
        # Update database
        for round in self._rounds:
            round_to_add = {"name": round.get_name}
            round_to_add["date_begin"] = round.get_begin
            round_to_add["date_end"] = round.get_end
            matchs = []
            for match in round.get_matchs:
                match_to_add = {
                    "player_1": match.get_players[0].get_player,
                    "player_2": match.get_players[1].get_player,
                    "score_player_1": match.get_scores[0],
                    "score_player_2": match.get_scores[1]}
                matchs.append(match_to_add)
            round_to_add.update({"matchs": matchs})
            rounds.append(round_to_add)
        tournament_db = Db_manager_tournament()
        tournament_db.update_rounds_by_name_and_date(
            self._name, self._date, rounds)

    def add_player(self, player_id: int) -> None:
        """Add player id to players dict, set score to 0 and save in database

        Args:
            player_id (int): Player's id

        """
        self._players[str(player_id)] = 0
        self.save_players()

    def update_player_point(self, player_id, points) -> None:
        """Add points and save in database

        Args:
            player_id (int): Player to add points
            points (int): Points to add

        """
        self._players[str(player_id)] = self._players[str(player_id)] + points
        self.save_players()

    def save_players(self) -> None:
        """Save players dict in database by tournament name and date

        """
        tournament_db = Db_manager_tournament()
        tournament_db.update_players_by_name_and_date(
            self._name, self._date, self._players)

    def save_db(self) -> bool | int:
        """Save tournament in database and get is id

        Args:
            self:   name (str): Tournament's name
                    place (srt): Tournament's place
                    date (str): Tournament's date
                    round (int): Number of round for the tournament
                    time_ctrl (str): Bullet, Blitz, Rapid, only one of them
                    description (str): General description
                    rounds (list): List of Round object
                    players (dict): Key = player's id on database, \
value = player's points for this tournament
        """
        tournament_db = Db_manager_tournament()
        return tournament_db.add_one(self)

    def get_points(self, player_id: int) -> int:
        """Get points for a player

        Args:
            player_id (int): Player's id

        Return:
            int: Points of the player

        """
        return self._players[str(player_id)]

    @property
    def get_id(self) -> int:
        return self._id

    @property
    def get_tournament(self) -> dict:
        tournament_dict = {
            "name": self._name,
            "place": self._place,
            "date": self._date,
            "round": self._round,
            "time_ctrl": self._time_ctrl,
            "description": self._description,
            "rounds": self._rounds,
            "players": self._players,
            "status": self._status
        }
        return tournament_dict

    @property
    def get_status(self) -> bool:
        return self._status

    @property
    def get_players(self) -> dict:
        """Property dict of player id: points

        Return:
            dict: Key = player_id in database, \
value = points in this tournament

        """
        return self._players

    @property
    def get_rounds(self) -> list[Round]:
        """Property list of rounds

        Return:
            list: rounds in this tournament

        """
        return self._rounds

    @property
    def get_matchs_already_played(self) -> List[Match]:
        """Property list of match already played on this tournament

        Return:
            list: list[Match]

        """
        matchs_played: List[Match] = []
        for round in self._rounds:
            round: Round = round
            for match in round.get_matchs:
                matchs_played.append(match)
        return matchs_played

    def __str__(self) -> str:
        """Human readable Tournament for dev only

        Return:
            str: Tournament
        """
        return f"Le tournoi: {self._name} en date du {self._date}\n\
s'est déroulé à: {self._place} \
et à réuni {len(self._players)} participants.\n\
Le time control est {self._time_ctrl} la description est {self._description}."

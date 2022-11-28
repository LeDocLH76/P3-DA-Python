from typing import List

from models.match import Match
from models.round import Round
from models.db_manager_tournaments import Db_manager_tournament
from utils.constant import ROUND_QUANTITY


class Tournament:
    def __init__(self,
                 name,
                 place,
                 date,
                 time_ctrl,
                 description,
                 round=ROUND_QUANTITY
                 ):
        """Tournament definition

        Attributes:
            name (str): Tournament's name
            place (srt): Tournament's place
            date (str): Tournament's date
            round (int): Number of round for the tournament \
            by default ROUND_QUANTITY
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
        self._id = None

    @classmethod
    def add_tournament_from_db(cls, tournament_id: int):
        """Alternative __init__ to create Tournament from database

        Args:
            tournament_id (int): Tournament's id to rebuild

        Return:
            object: Tournament
        """
        manager_tournament_obj = Db_manager_tournament()
        tournament_obj = manager_tournament_obj.get_one_from_db(tournament_id)
        return tournament_obj

    def set_date(self, date: str) -> None:
        """Set tournament's date

        Args:
            date (str): Date for this tournament

        """
        self._date = date

    def set_status(self, new_status: bool) -> None:
        self._status = new_status
        self.save_status()

    def set_round(self, new_round_quantity) -> None:
        self._round = new_round_quantity
        self.save_round_quantity()

    def set_id(self, tournament_id) -> None:
        self._id = tournament_id

    def update_round(self, round: Round = None) -> None:
        """Update rounds in database, add round before if not None.

        Args:
            round (Round or None): If not None, add the round before

        """
        if round is not None:
            self._rounds.append(round)
        manager_tournament_obj = Db_manager_tournament()
        manager_tournament_obj.update_rounds_by_tournament_id(self)

    def add_round_from_db(self, round: Round) -> None:
        self._rounds.append(round)

    def add_player_from_db(self, player_id, player_points) -> None:
        self._players[str(player_id)] = player_points

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
        manager_tournament_obj = Db_manager_tournament()
        manager_tournament_obj.update_players_by_tournament_id(
            self)

    def save_round_quantity(self) -> None:
        """Save round quantity in database by tournament id

        """
        manager_tournament_obj = Db_manager_tournament()
        manager_tournament_obj.update_round_quantity_by_tournament_id(self)

    def save_status(self):
        manager_tournament_obj = Db_manager_tournament()
        manager_tournament_obj.update_status_by_tournament_id(self)

    def save_on_db(self) -> bool | int:
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
                    status (bool): Tournament's status
        """
        manager_tournament_obj = Db_manager_tournament()
        return manager_tournament_obj.add_one(self)

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
    def get_name(self) -> str:
        return self._name

    @property
    def get_round(self) -> int:
        return self._round

    @property
    def get_tournament(self) -> dict:
        """Get tournament base info

        Return:
            dict:"name": tournament's name,
                "place": tournament's place,
                "date": tournament's date,
                "round": tournament's round,
                "time_ctrl": tournament's time_ctrl,
                "description": tournament's description,
                "rounds": [tournament's rounds],
                "players": {tournament's players},
                "status": tournament's status

        """
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
        if self._id is not None:
            tournament_dict['id'] = self._id
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

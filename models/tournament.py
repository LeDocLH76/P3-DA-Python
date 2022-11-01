from typing import List

from models.match import Match
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
        self.set_id_save_db()

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

    def update_player_point_from_db(self, player_id, points) -> None:
        """Update player's points from database

        Args:
            player_id (int): Key for players dict, \
                it's the player's id on database.
            points (int): Value for players dict, \
                player's points for this tournament.

        """
        self._players[str(player_id)] = points

    def add_rounds_from_bd(self, rounds) -> None:
        """Add round from database

        Args:
            rounds (list): Round list for this tournament

        """
        self._rounds = rounds

    def set_date(self, date: str) -> None:
        """Set tournament's date

        Args:
            date (str): Date for this tournament

        """
        self._date = date

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
        """Save players dict in database

        """
        tournament_db = Db_manager_tournament()
        tournament_db.update_players_by_name_and_date(
            self._name, self._date, self._players)

    def set_id_save_db(self) -> None:
        """Save tournament in database and get id on database

        Args:
            name (str): Tournament's name
            place (srt): Tournament's place
            date (str): Tournament's date
            round (int): Number of round for the tournament
            time_ctrl (str): Bullet, blitz, rapid, only one of them
            description (str): General description
            rounds (list): List of Round object
            players (dict): Key = player's id on database, \
value = player's points for this tournament

        """
        tournament_dict = {
            "name": self._name,
            "place": self._place,
            "date": self._date,
            "round": self._round,
            "time_ctrl": self._time_ctrl,
            "description": self._description,
            "rounds": self._rounds,
            "players": self._players
        }
        tournament_db = Db_manager_tournament()
        self._id = tournament_db.add_one(tournament_dict)

    def get_points(self, player_id) -> int:
        """Get points for a player

        Args:
            player_id (int): Player's id

        Return:
            int: Points of the player

        """
        return self._players[str(player_id)]

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
        return f"Le tournois: {self._name} en date du {self._date}\n\
s'est déroulé à: {self._place} \
et à réuni {len(self._players)} participants.\n\
Le time control est {self._time_ctrl} la description est {self._description}."

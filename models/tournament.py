from typing import List

from tinydb import TinyDB, where

from models.match import Match
from models.round import Round


class Tournament:
    def __init__(self, name, place, date, time_ctrl, description, round=4):
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
                               round=4):
        tournament = cls.__new__(cls)
        tournament._name = name
        tournament._place = place
        tournament._date = date
        tournament._time_ctrl = time_ctrl
        tournament._description = description
        tournament._players = players
        tournament._round = round
        return tournament

    def update_player_point_from_db(self, player_id, points):
        self._players[str(player_id)] = points

    def add_rounds_from_bd(self, rounds):
        self._rounds = rounds

    def set_date(self, date: str):
        self._date = date

    def update_round(self, round: Round = None):
        if round is not None:
            self._rounds.append(round)
        rounds = []
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
        db = TinyDB('chess_tournament')
        tournaments_table = db.table("tournaments")
        tournaments_table.update({"rounds": rounds},
                                 (where("name") == self._name)
                                 & (where("date") == self._date))

    def add_player(self, player_id: int):
        self._players[str(player_id)] = 0
        db = TinyDB('chess_tournament')
        tournaments_table = db.table("tournaments")
        tournaments_table.update({"players": self._players},
                                 (where("name") == self._name)
                                 & (where("date") == self._date))

    def update_player_point(self, player_id, points):
        self._players[str(player_id)] = self._players[str(player_id)] + points
        db = TinyDB('chess_tournament')
        tournaments_table = db.table("tournaments")
        tournaments_table.update({"players": self._players},
                                 (where("name") == self._name)
                                 & (where("date") == self._date))

    def set_id_save_db(self):
        tournament_json = {
            "name": self._name,
            "place": self._place,
            "date": self._date,
            "round": self._round,
            "time_ctrl": self._time_ctrl,
            "description": self._description,
            "rounds": self._rounds,
            "players": self._players
        }
        db = TinyDB('chess_tournament')
        tournaments_table = db.table("tournaments")
        self._id = tournaments_table.insert(tournament_json)

    def get_points(self, player_id):
        return self._players[str(player_id)]

    @property
    def get_players(self):
        return self._players

    @property
    def get_rounds(self):
        return self._rounds

    @property
    def get_matchs_already_played(self) -> List[Match]:
        matchs_played: List[Match] = []
        for round in self._rounds:
            round: Round = round
            for match in round.get_matchs:
                matchs_played.append(match)
        return matchs_played

    def __str__(self):
        return f"Le tournois: {self._name} en date du {self._date}\n\
s'est déroulé à: {self._place} \
et à réuni {len(self._players)} participants.\n\
Le time control est {self._time_ctrl} la description est {self._description}."

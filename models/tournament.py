from typing import List

from models.match import Match
from models.round import Round


class Tournament:
    def __init__(self, name, place, date, time_ctrl, description, round=4):
        self._name = name
        self._place = place
        self.set_date(date)
        self.round = round
        self._time_ctrl = time_ctrl
        self._description = description
        self._rounds = []
        self._players = []

    def set_date(self, date):
        self._date = date

    def add_round(self, round):
        self._rounds.append(round)

    def add_player(self, player):
        self._players.append(player)

    @property
    def get_players(self):
        return self._players

    @property
    def get_round(self):
        return self._rounds

    @property
    def get_matchs_already_played(self):
        matchs_played: List[Match] = []
        for round in self._rounds:
            round: Round = round
            for match in round.get_round._matchs:
                matchs_played.append(match)
        return matchs_played

    def __str__(self):
        return f"Le tournois: {self._name} en date du {self._date}\n\
s'est déroulé à: {self._place} et à réunis {len(self._players)} participants."

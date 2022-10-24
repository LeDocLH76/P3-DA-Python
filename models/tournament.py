from typing import List

from tinydb import Query, TinyDB, where

from models.match import Match
from models.player import Player
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
        self._players: List[Player] = []

    def set_date(self, date: str):
        self._date = date

    def add_round(self, round: Round):
        self._rounds.append(round)

    def add_player(self, player: Player):
        self._players.append(player)

    def save_db(self):
        tournament_json = {
            "name": self._name,
            "place": self._place,
            "date": self._date,
            "round": self._round,
            "time_ctrl": self._time_ctrl,
            "description": self._description,
            "rounds": []
        }
        db = TinyDB('chess_tournament')
        tournaments_table = db.table("tournament")

        tournament = Query()
        if not tournaments_table.search((tournament.name == self._name)
                                        & (tournament.date == self._date)):
            tournaments_table.insert(tournament_json)
        else:
            print("Cet enregistrement est déja présent en base!")

    def update_round_db(self):
        rounds = []
        for round in self._rounds:
            round_name = round.get_name
            round_to_add = {"name": round_name}
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
        # print(rounds)

        db = TinyDB('chess_tournament')
        tournaments_table = db.table("tournament")

        tournaments_table.update({"rounds": rounds},
                                 (where("name") == self._name)
                                 & (where("date") == self._date))

    @property
    def get_players(self):
        return self._players

    @property
    def get_round(self):
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
et à réunis {len(self._players)} participants.\n\
Le time control est {self._time_ctrl} la description est {self._description}."

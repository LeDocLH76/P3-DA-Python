from typing import List
from models.player import Player


class Match:
    def __init__(self,
                 player1,
                 player2,
                 score_player1=None,
                 score_player2=None):
        self._player1 = player1
        self._player2 = player2
        self._score_player1 = score_player1
        self._score_player2 = score_player2

    def set_score(self, score_player1, score_player2):
        self._score_player1 = score_player1
        self._score_player2 = score_player2

    @property
    def get_match(self):
        match = ([self._player1, self._score_player1],
                 [self._player2, self._score_player2])
        return match

    @property
    def get_players(self) -> List[Player]:
        players: List[Player] = [self._player1, self._player2]
        return players

    @property
    def get_scores(self):
        scores = [self._score_player1, self._score_player2]
        return scores

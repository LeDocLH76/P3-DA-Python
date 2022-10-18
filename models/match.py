from typing import List
from models.player import Player


class Match:
    def __init__(self,
                 player1,
                 player2,
                 score_player1=None,
                 score_player2=None):
        self._player1: Player = player1
        self._player2: Player = player2
        self._score_player1: int | None = score_player1
        self._score_player2: int | None = score_player2

    def set_score(self, score_player1: int, score_player2: int):
        self._score_player1 = score_player1
        self._score_player2 = score_player2

    @property
    def get_match(self) -> tuple[list[Player], list[Player]]:
        match: tuple[list[Player], list[Player]] = (
            [self._player1, self._score_player1],
            [self._player2, self._score_player2])
        return match

    @property
    def get_players(self) -> List[Player]:
        players: List[Player] = [self._player1, self._player2]
        return players

    @property
    def get_scores(self) -> List[int | None]:
        scores: List[int | None] = [self._score_player1, self._score_player2]
        return scores

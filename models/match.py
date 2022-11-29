
from typing import List

from models.player import Player


class Match:
    """Match definition

    Attributes:
        player1 (Player): First player on match
        player2 (Player): Second player on match
        score_player1 (int or None): First player's score on match
        score_player2 (int or None): Second player's score on match

    """

    def __init__(self,
                 player1: Player,
                 player2: Player,
                 score_player1: float | None = None,
                 score_player2: float | None = None):
        self._player1 = player1
        self._player2 = player2
        self._score_player1 = score_player1
        self._score_player2 = score_player2

    def set_score(self, score_player1: float, score_player2: float) -> None:
        """Set score for 2 players

        Args:
            score_player1 (int): Player1's score
            score_player2 (int): Player1's score

        """
        self._score_player1 = score_player1
        self._score_player2 = score_player2

    @property
    def get_match(self) -> tuple[list[Player | float | None], list[Player | float | None]]:
        """Property match's datas

        Return:
            tuple: ([player1, score_player1],[player2, score_player2])"""
        match: tuple[list[Player | float | None], list[Player | float | None]] = (
            [self._player1, self._score_player1],
            [self._player2, self._score_player2]
        )
        return match

    @property
    def get_players(self) -> List[Player]:
        """Property match's players

        Return:
            list: [player1, player2]

        """
        players: List[Player] = [self._player1, self._player2]
        return players

    @property
    def get_scores(self) -> List[float | None]:
        """Property match's scores

        Return:
            list: [score_player1, score_player2]

        """
        scores: List[float | None] = [self._score_player1, self._score_player2]
        return scores

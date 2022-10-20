from typing import List

from models.match import Match


class Round:
    def __init__(self, name):
        self._name = name
        self._matchs: List[Match] = []

    def add_match(self, match):
        self._matchs.append(match)

    def set_begin(self, begin):
        self._date_begin = begin

    def set_end(self, end):
        self._date_end = end

    @property
    def get_matchs(self) -> List[Match]:
        return self._matchs

    @property
    def get_name(self) -> str:
        return self._name

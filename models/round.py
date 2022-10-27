from datetime import datetime
import time
from typing import List

from models.match import Match


class Round:
    def __init__(self, name):
        self._name = name
        self._matchs: List[Match] = []
        self.set_begin()

    @classmethod
    def add_round_from_db(cls, name, date_begin, date_end):
        round = cls.__new__(cls)
        round._name = name
        round._date_begin = date_begin
        round._date_end = date_end
        round._matchs = []
        return round

    def add_match(self, match):
        self._matchs.append(match)

    def set_begin(self):
        ts = time.time()
        begin = datetime. fromtimestamp(ts).isoformat()
        self._date_begin = begin

    def set_end(self, ts):
        self._date_end = datetime. fromtimestamp(ts).isoformat()

    @property
    def get_matchs(self) -> List[Match]:
        return self._matchs

    @property
    def get_name(self) -> str:
        return self._name

    @property
    def get_begin(self) -> str:
        return self._date_begin

    @property
    def get_end(self) -> str:
        return self._date_end

    def __str__(self) -> str:
        begin_obj = datetime.fromisoformat(self._date_begin)
        end_obj = datetime.fromisoformat(self._date_end)
        return f"{self._name} \
Début: {begin_obj.day}/{begin_obj.month}/{begin_obj.year} \
{begin_obj.hour}:{begin_obj.minute}:{begin_obj.second} \
Fin: {end_obj.day}/{end_obj.month}/{end_obj.year} \
{end_obj.hour}:{end_obj.minute}:{end_obj.second} \
Match: {len(self._matchs)}"

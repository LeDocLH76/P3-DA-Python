from datetime import datetime
import time
from typing import List

from models.match import Match


class Round:
    """Round definition

    Attributes:
        name (str): round's name

    """

    def __init__(self, name):
        self._name = name
        self._matchs: List[Match] = []
        self.set_begin()
        self._date_end = None

    @classmethod
    def add_round_from_db(cls, name, date_begin, date_end=None):
        """Alternative __init__ to create Round from database

        Args:
            name (str): Round's name
            date_begin (str): Round's begin date and time like iso format
            date_end (str): Round's end date and time like iso format
            matchs (list): Round's matchs list empty at the beginning

        """
        round = cls.__new__(cls)
        round._name = name
        round._date_begin = date_begin
        if date_end is not None:
            round._date_end = date_end
        round._matchs = []
        return round

    def add_match(self, match) -> None:
        """Add a match to the matchs list

        Args:
            match (Match): Match to add to the list

        """
        self._matchs.append(match)

    def set_begin(self):
        """Set the beginning of the round

        date_begin(str): round's begin date and time like iso format

        """
        ts = time.time()
        begin = datetime. fromtimestamp(ts).isoformat()
        self._date_begin = begin

    def set_end(self, ts):
        """Set the end of the round

        date_end(str): round's end date and time like iso format

        Args:
            ts (float): Timestamp to convert

        """
        self._date_end = datetime. fromtimestamp(ts).isoformat()

    @property
    def get_matchs(self) -> List[Match | None]:
        """Property round's matchs list

        Return:
            list: Matchs in the round"""
        return self._matchs

    @property
    def get_name(self) -> str:
        """Property round'name

        Return:
            name (str): Name of the round

        """
        return self._name

    @property
    def get_begin(self) -> str:
        """Property round's beguinning

        Return:
            date_begin (str): Round's begin date and time like iso format

        """
        return self._date_begin

    @property
    def get_end(self) -> str | bool:
        """Property round's end

        Return:
            date_end (str | bool): Round's end date and time like iso format \
                if round is close, False if not

        """
        if self._date_end is not None:
            return self._date_end
        return False

    def __str__(self) -> str:
        """Human readable Round for dev only

        Return:
            str: Round datas

        """
        begin_obj = datetime.fromisoformat(self._date_begin)
        end_obj = datetime.fromisoformat(self._date_end)
        return f"{self._name} \
Début: {begin_obj.day}/{begin_obj.month}/{begin_obj.year} \
{begin_obj.hour}:{begin_obj.minute}:{begin_obj.second} \
Fin: {end_obj.day}/{end_obj.month}/{end_obj.year} \
{end_obj.hour}:{end_obj.minute}:{end_obj.second} \
Match: {len(self._matchs)}"

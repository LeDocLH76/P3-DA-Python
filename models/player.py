
from models.db_manager_players import Db_manager_player
from utils.transform_date import date_fr2iso, date_iso2fr


class Player:
    """ Player definition

    Attributes:
        name (str): Player's name
        surname (str): Player's surname
        birth_date (str): Player' birth date like dd/mm/yyyy
        gender (str): Player's gender only M of F
        classification (None or int): Player's classification
        id (int): Player's id on database

    """

    def __init__(self,
                 name: str,
                 surname: str,
                 birth_date: str,
                 gender: str,
                 classification=None):
        self._name = name
        self._surname = surname
        self.set_birth_date(birth_date)
        self._gender = gender.strip()[0].capitalize()
        self._classification = classification
        self._id = None

    @classmethod
    def add_player_from_db(cls,
                           name: str,
                           surname: str,
                           birth_date_iso: str,
                           gender: str,
                           classification: None | int,
                           id: int):
        """Alternative __init__ to create Player from database

        Args:
        name (str): Player's name
        surname (str): Player's surname
        birth_date (str): Player' birth date like yyyy-mm-dd
        gender (str): Player's gender only M of F
        classification (None or int): Player's classification
        id (int): Player's id on database

        """

        birth_date_fr = date_iso2fr(birth_date_iso)

        player = cls.__new__(cls)
        player._name = name
        player._surname = surname
        player._birth_date = birth_date_fr
        player._gender = gender
        player._classification = classification
        player._id = id
        return player

    def set_birth_date(self, birth_date: str) -> None:
        """Transform birth_date from dd/mm/yyyy to iso format yyyy-mm-dd

        Args:
            birth_date (str): date string like dd/mm/yyyy

        """
        self._birth_date = date_fr2iso(birth_date)

    def set_classification(self, classification: int) -> None:
        """Set Player's classification

        Args:
            classification (int): Player's classification to set

        """
        self._classification = classification
        player_bd = Db_manager_player()
        player_bd.update_classification_by_id(self._id, classification)

    def set_id(self, player_id) -> None:
        """Set Player's id
        """
        self._id = player_id

    @ property
    def get_id(self) -> int:
        """Property Player's id

        Return:
            int: Player's id on database

        """
        return self._id

    @ property
    def get_player(self) -> dict:
        """Property Player's datas

        Return:
            dict: name, surname, birth_date, gender, \
classification, id of the Player

        """
        player_dict = {
            "name": self._name,
            "surname": self._surname,
            "birth_date": self._birth_date,
            "gender": self._gender,
            "classification": self._classification
        }
        player_dict['id'] = self._id
        return player_dict

    def __str__(self) -> str:
        """Human readable Player for dev only

        Return:
            str: Player

        """
        classification = (self._classification if
                          self._classification is not None else "N/A")
        return f"{self._surname} {self._name} Né le: \
{self._birth_date} Classé: {classification}"

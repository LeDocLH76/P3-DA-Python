
from models.db_manager_players import Db_manager_player


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
        self.set_id_save_db()

    @classmethod
    def add_player_from_db(cls,
                           name: str,
                           surname: str,
                           birth_date: str,
                           gender: str,
                           classification: None | int,
                           id: int):
        """Alternative __init__ for create Player from database

        Args:
        name (str): Player's name
        surname (str): Player's surname
        birth_date (str): Player' birth date like dd/mm/yyyy
        gender (str): Player's gender only M of F
        classification (None or int): Player's classification
        id (int): Player's id on database

        """
        player = cls.__new__(cls)
        player._name = name
        player._surname = surname
        player._birth_date = birth_date
        player._gender = gender
        player._classification = classification
        player._id = id
        return player

    def set_birth_date(self, birth_date: str) -> None:
        """Transform birth_date from dd/mm/yyyy to iso format yyyy-mm-dd

        Args:
            birth_date (str): date string like dd/mm/yyyy

        """
        birth_date_list = birth_date.split("/")
        if len(birth_date_list[0]) < 2:
            birth_date_list[0] = "0" + birth_date_list[0]
        if len(birth_date_list[1]) < 2:
            birth_date_list[1] = "0" + birth_date_list[1]
        birth_date_invert_list = reversed(birth_date_list)
        birth_date_iso = "-".join(birth_date_invert_list)
        self._birth_date = birth_date_iso

    def set_classification(self, classification: int) -> None:
        """Set Player's classification

        Args:
            classification (int): Player's classification to set

        """
        self._classification = classification
        player_bd = Db_manager_player()
        player_bd.update_classification_by_id(self._id, classification)

    def set_id_save_db(self) -> None:
        """Save Player from get_player on database and get is id

        """
        player_db = Db_manager_player()
        self._id = player_db.add_one(self.get_player)

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
classification of the Player

        """
        player = {"name": self._name,
                  "surname": self._surname,
                  "birth_date": self._birth_date,
                  "gender": self._gender,
                  "classification": self._classification}
        return player

    def __str__(self) -> str:
        """Human readable Player for dev only

        Return:
            str: Player

        """
        classification = (self._classification if
                          self._classification is not None else "N/A")
        return f"{self._surname} {self._name} Né le: \
{self._birth_date} Classé: {classification}"

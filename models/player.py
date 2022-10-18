
# from datetime import date
from tinydb import TinyDB, Query, where


class Player:
    """ Player definition """

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
        self._points = 0

    def set_birth_date(self, birth_date: str) -> None:
        # format and transform birth_date
        # print(birth_date)
        birth_date_list = birth_date.split("/")
        if len(birth_date_list[0]) < 2:
            birth_date_list[0] = "0" + birth_date_list[0]
        if len(birth_date_list[1]) < 2:
            birth_date_list[1] = "0" + birth_date_list[1]
        # print(birth_date_list)
        birth_date_invert_list = reversed(birth_date_list)
        # print(birth_date_invert_list)
        birth_date_iso = "-".join(birth_date_invert_list)
        # print(birth_date_iso)
        # **************************
        # non compatible avec tinydb
        # birth_date_obj = date.fromisoformat(birth_date_iso)
        # print(birth_date_obj, type(birth_date_obj))
        # **************************
        self._birth_date = birth_date_iso

    def set_classification(self, classification) -> None:
        self._classification = classification

    def add_point(self, point) -> None:
        self._points += point

    def save_db(self) -> None:
        db = TinyDB('chess_tournament')
        players_table = db.table("players")
        player = Query()
        if not players_table.search((player.name == self._name)
                                    & (player.surname == self._surname)
                                    & (player.birth_date == self._birth_date)):
            players_table.insert(self.get_player)
        else:
            print("Cet enregistrement est déja présent en base!")

    def update_classification_db(self, classification):
        db = TinyDB('chess_tournament')
        players_table = db.table("players")
        players_table.update({"classification": classification},
                             (where("name") == self._name)
                             & (where("surname") == self._surname)
                             & (where("birth_date") == self._birth_date))

    def update_points_db(self, points):
        db = TinyDB('chess_tournament')
        players_table = db.table("players")
        players_table.update({"points": points},
                             (where("name") == self._name)
                             & (where("surname") == self._surname)
                             & (where("birth_date") == self._birth_date))

    @ property
    def get_player(self) -> dict:
        player = {"name": self._name,
                  "surname": self._surname,
                  "birth_date": self._birth_date,
                  "gender": self._gender,
                  "classification": self._classification,
                  "points": self._points}
        return player

    def __str__(self) -> str:
        classification = (self._classification if
                          self._classification is not None else "N/A")
        return f"{self._surname} {self._name}\nNé le: \
{self._birth_date} Classé: {classification}"

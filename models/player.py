
from tinydb import Query, TinyDB, where


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
        self.set_id_save_db()

    @classmethod
    def add_player_from_db(cls,
                           name: str,
                           surname: str,
                           birth_date: str,
                           gender: str,
                           classification,
                           id):
        player = cls.__new__(cls)
        player._name = name
        player._surname = surname
        player._birth_date = birth_date
        player._gender = gender
        player._classification = classification
        player._id = id
        return player

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
        db = TinyDB('chess_tournament')
        players_table = db.table("players")
        players_table.update({"classification": classification},
                             (where("name") == self._name)
                             & (where("surname") == self._surname)
                             & (where("birth_date") == self._birth_date))

    def set_id_save_db(self) -> None:
        db = TinyDB('chess_tournament')
        players_table = db.table("players")
        print("Sauve le joueur en Db et recupère sont id")
        print(f"Player = {self.get_player}")

        # Vérifie si le joueur est déja enregistré
        player = Query()
        if not players_table.search(
            (player.name == self._name)
            & (player.surname == self._surname)
                & (player.birth_date == self._birth_date)):
            self._id = players_table.insert(self.get_player)
        else:
            print("Cet enregistrement est déja présent en base!")
            # Find player_id on Db, put it in self
            player_db = players_table.get(
                (where("name") == self._name)
                & (where("surname") == self._surname)
                & (where("birth_date") == self._birth_date))
            self._id = player_db.doc_id
        print(f"Id du joueur ={self._id}")

    @ property
    def get_id(self) -> int:
        return self._id

    @ property
    def get_player(self) -> dict:
        # Points n'est plus ici
        player = {"name": self._name,
                  "surname": self._surname,
                  "birth_date": self._birth_date,
                  "gender": self._gender,
                  "classification": self._classification}
        return player

    def __str__(self) -> str:
        classification = (self._classification if
                          self._classification is not None else "N/A")
        return f"{self._surname} {self._name} Né le: \
{self._birth_date} Classé: {classification}"

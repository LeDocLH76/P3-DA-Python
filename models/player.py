
from datetime import date


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

    def set_birth_date(self, birth_date: str) -> None:
        # format and transform birth_date
        birth_date_list = birth_date.split("/")
        birth_date_invert_list = reversed(birth_date_list)
        birth_date_iso = "-".join(birth_date_invert_list)
        birth_date_obj = date.fromisoformat(birth_date_iso)
        # print(birth_date, type(birth_date))
        self._birth_date = birth_date_obj

    def set_classification(self, classification) -> None:
        self._classification = classification

    @ property
    def get_player(self) -> dict:
        player = {"name": self._name,
                  "surname": self._surname,
                  "birth_date": self._birth_date,
                  "gender": self._gender,
                  "classification": self._classification}
        return player

    def __str__(self) -> str:
        classification = (self._classification if
                          self._classification is not None else "N/A")
        return f"{self._surname} {self._name}\nNé le: \
{self._birth_date} Classé: {classification}"


if __name__ == "__main__":
    joueur = Player("BONNOT", "Jean", "01/06/2022", "M")
    print(joueur.get_player)
    print(joueur.get_player["name"])
    print([key for key in joueur.get_player])
    print([joueur.get_player[key] for key in joueur.get_player])
    print(joueur)
    joueur.set_classification(1)
    print(joueur)

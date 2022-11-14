from tinydb import Query, TinyDB, where


class Db_manager_tournament:
    def __init__(self):
        db = TinyDB('chess_tournament')
        self.tournaments_table = db.table("tournaments")

    def get_all(self):
        from models.tournament import Tournament
        tournaments_obj_list: list[Tournament] = []
        for document in self.tournaments_table:
            tournament_id = document.doc_id
            tournament_obj = self.get_one(tournament_id)
            tournaments_obj_list.append(tournament_obj)
        return tournaments_obj_list

    def get_players_by_id(self, tournament_id: int) -> dict:
        tournament = self.tournaments_table.get(doc_id=tournament_id)
        player_dict: dict = tournament.get('players')
        return player_dict

    def get_players_all(self) -> set[int]:
        tournaments_obj_list = self.get_all()
        players_set: set[int] = set()
        for tournament_obj in tournaments_obj_list:
            players_dict = self.get_players_by_id(tournament_obj.get_id)
            players_set.update(players_dict)
        return players_set

    def get_one(self, tournament_id):
        from models.tournament import Tournament
        document = self.tournaments_table.get(doc_id=tournament_id)
        tournament_obj = Tournament(
            document["name"],
            document["place"],
            document["date"],
            document["time_ctrl"],
            document["description"],
            document["round"]
        )
        tournament_obj.set_id(document.doc_id)
        tournament_obj.set_status(document["status"])
        tournament_obj.set_players_from_db(document["players"])
        tournament_obj.set_rounds_from_db(document["rounds"])
        return tournament_obj

    def get_rounds_by_id(self, tournament_id: int):
        tournament = self.tournaments_table.get(doc_id=tournament_id)
        rounds_list = tournament.get('rounds')
        return rounds_list

    def update_players_by_name_and_date(
            self, tournament_name, tournament_date, players_data_list):
        self.tournaments_table.update({"players": players_data_list},
                                      (where("name") == tournament_name)
                                      & (where("date") == tournament_date))

    def add_one(self, tournament_obj) -> bool | int:
        from models.tournament import Tournament
        tournament_obj: Tournament = tournament_obj
        tournament_dict = tournament_obj.get_tournament
        tournament = Query()
        # tournament exist ?
        if not self.tournaments_table.search(
            (tournament.name == tournament_dict["name"])
                & (tournament.date == tournament_dict["date"])):
            # Create tournament in db and get id
            tournament_id = self.tournaments_table.insert(tournament_dict)
            tournament_obj.set_id(tournament_id)
            return True
        else:
            # Tournament already exist, find is id and return it
            tournament_db = self.tournaments_table.get(
                (tournament.name == tournament_dict["name"])
                & (tournament.date == tournament_dict["date"]))
            tournament_id = tournament_db.doc_id
        return tournament_id

    def update_rounds_by_name_and_date(
            self, tournament_name, tournament_date, rounds_dict):
        self.tournaments_table.update({"rounds": rounds_dict},
                                      (where("name") == tournament_name)
                                      & (where("date") == tournament_date))

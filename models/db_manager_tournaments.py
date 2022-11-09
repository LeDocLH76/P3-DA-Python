from tinydb import Query, TinyDB, where


class Db_manager_tournament:
    def __init__(self):
        db = TinyDB('chess_tournament')
        self.tournaments_table = db.table("tournaments")

    def get_all(self) -> list[dict]:
        tournaments_list: list[dict] = []
        for document in self.tournaments_table:
            tournament = {}
            tournament["id"] = document.doc_id
            tournament["name"] = document["name"]
            tournament["date"] = document["date"]
            tournament["description"] = document["description"]
            tournaments_list.append(tournament)
        return tournaments_list

    def get_players_by_id(self, tournament_id: int) -> list[int]:
        tournament = self.tournaments_table.get(doc_id=tournament_id)
        player_list: list[int] = tournament.get('players')
        return player_list

    def get_players_all(self) -> list[int]:
        tournaments_list = self.get_all()
        players_set = set()
        for tournament in tournaments_list:
            players = self.get_one(tournament["id"])["players"]
            players_set.update(players)
            players_set = {int(item) for item in players_set}
        return players_set

    def get_one(self, tournament_id):
        tournament_db = self.tournaments_table.get(doc_id=tournament_id)
        tournament = {}
        tournament["name"] = tournament_db["name"]
        tournament["place"] = tournament_db["place"]
        tournament["date"] = tournament_db["date"]
        tournament["time_ctrl"] = tournament_db["time_ctrl"]
        tournament["description"] = tournament_db["description"]
        tournament["players"] = tournament_db["players"]
        tournament["round"] = tournament_db["round"]
        return tournament

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

from tinydb import TinyDB, where


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

    def add_one(self, tournament_dict):
        tournament_id = self.tournaments_table.insert(tournament_dict)
        return tournament_id

    def update_rounds_by_name_and_date(self, tournament_name, tournament_date, rounds_dict):
        self.tournaments_table.update({"rounds": rounds_dict},
                                      (where("name") == tournament_name)
                                      & (where("date") == tournament_date))

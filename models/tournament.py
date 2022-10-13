from typing import List


class Tournament:
    def __init__(self, name, place, date, time_ctrl, description, round=4):
        self._name = name
        self._place = place
        self.set_date(date)
        self.round = round
        self._time_ctrl = time_ctrl
        self._description = description
        self._rounds = []
        self._players = []

    def set_date(self, date):
        self._date = date

    def add_round(self, round):
        self._rounds.append(round)

    def add_player(self, player):
        self._players.append(player)

    @property
    def get_tournament(self):
        return f"Le tournois: {self._name} en date du {self._date}\n\
s'est déroulé à: {self._place} et à réunis {len(self._players)} participants."

    @property
    def get_players(self):
        return self._players

    @property
    def get_round(self):
        return self._rounds

    @property
    def get_matchs_already_played(self):
        matchs_played: List[Match] = []
        for round in self._rounds:
            round: Round = round
            for match in round.get_round._matchs:
                matchs_played.append(match)
        return matchs_played


if __name__ == "__main__":
    from player import Player
    from match import Match
    from round import Round
    tournament = Tournament("T1", "Ici", "10/10/2022",
                            "Rapid", "Mon premier tournois")
    player01 = Player("QUIROUL", "Pierre", "05/12/1980", "M")
    player02 = Player("BONOD", "Jean", "01/04/1902", "M")
    player03 = Player("IMAL", "Anne", "15/10/1986", "F")
    player04 = Player("HOL", "Lucie", "08/02/1945", "F")
    tournament.add_player(player01)
    tournament.add_player(player02)
    tournament.add_player(player03)
    tournament.add_player(player04)
    match1 = Match(player01, player02)
    match1.set_score(1, 0)
    match2 = Match(player03, player04)
    match2.set_score(0, 1)
    round1 = Round("Round-1")
    round1.add_match(match1)
    round1.add_match(match2)
    tournament.add_round(round1)
    print(tournament.get_tournament)
    print(tournament.get_round)
    print(tournament.get_players)
    print(tournament.get_matchs_already_played)

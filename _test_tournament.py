from tinydb import TinyDB

from models.player import Player
from models.match import Match
from models.round import Round
from models.tournament import Tournament

db = TinyDB('chess_tournament')
db.drop_tables()

tournament = Tournament("T1", "Ici", "10/10/2022",
                        "Rapid", "Mon premier tournois")
player01 = Player("QUIROUL", "Pierre", "05/12/1980", "M")
tournament.add_player(player01.get_id)
player02 = Player("BONOD", "Jean", "01/04/1902", "M")
tournament.add_player(player02.get_id)
player03 = Player("IMAL", "Anne", "15/10/1986", "F")
tournament.add_player(player03.get_id)
player04 = Player("HOL", "Lucie", "08/02/1945", "F")
tournament.add_player(player04.get_id)
match1 = Match(player01, player02)
match1.set_score(1, 0)
match2 = Match(player03, player04)
match2.set_score(0, 1)
round1 = Round("Round-1")
round1.add_match(match1)
round1.add_match(match2)
tournament.add_round(round1)
# print(tournament)
# print(tournament.get_round)
# print(tournament.get_players)
# print(tournament.get_matchs_already_played)

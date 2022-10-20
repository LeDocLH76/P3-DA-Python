from models.player import Player
from models.match import Match
from models.round import Round

player01 = Player("QUIROUL", "Pierre", "05/12/1980", "M")
player02 = Player("BONOD", "Jean", "01/04/1902", "M")
player03 = Player("IMAL", "Anne", "15/10/1986", "F")
player04 = Player("HOL", "Lucie", "08/02/1945", "M")
match1 = Match(player01, player02)
match1.set_score(1, 0)
match2 = Match(player03, player04)
match2.set_score(0, 1)
round1 = Round("Round-1")
round1.add_match(match1)
round1.add_match(match2)
print(match1.get_players[0], match1.get_scores[0])
print(match1.get_players[1], match1.get_scores[1])
print(match2.get_players[0], match1.get_scores[0])
print(match2.get_players[1], match1.get_scores[1])
print(round1.get_round._matchs)

from models.player import Player
from models.match import Match

player1 = Player("QUIROUL", "Pierre", "05/12/1980", "M")
player2 = Player("BONOD", "Jean", "01/04/1902", "M")
print(player1)
print(player2)
match1 = Match(player1, player2)
print(match1.get_match)
print(match1.get_players[0], match1.get_scores[0])
print(match1.get_players[1], match1.get_scores[1])
match1.set_score(1, 0)
match1.get_players[0].set_classification(1)
match1.get_players[1].set_classification(3)
print(f"{match1.get_players[0]}, Score: {match1.get_scores[0]}")
print(f"{match1.get_players[1]}, Score: {match1.get_scores[1]}")
print(match1.get_match)

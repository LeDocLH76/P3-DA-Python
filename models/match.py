class Match:
    def __init__(self, player1, player2):
        self.set_match(player1, player2)
        self.set_score()

    def set_match(self, player1, player2):
        self._player1 = player1
        self._player2 = player2

    def set_score(self, score_player1=None, score_player2=None):
        self._score_player1 = score_player1
        self._score_player2 = score_player2

    @property
    def get_match(self):
        match = ([self._player1, self._score_player1],
                 [self._player2, self._score_player2])
        return match

    @property
    def get_players(self):
        players = [player1, player2]
        return players

    @property
    def get_scores(self):
        scores = [self._score_player1, self._score_player2]
        return scores


if __name__ == "__main__":
    from player import Player
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
    print(match1.get_players[0], match1.get_scores[0])
    print(match1.get_players[1], match1.get_scores[1])
    print(match1.get_match)

import time
from tinydb import TinyDB

from models.player import Player
from models.match import Match
from models.round import Round
from models.tournament import Tournament

db = TinyDB('chess_tournament')
# db.drop_tables()


def save_player(player_obj):
    from models.db_manager_players import Db_manager_player
    manager_player_obj = Db_manager_player()
    manager_player_obj.add_one(player_obj)


tournament = Tournament("T1", "Ici", "10/10/2022",
                        "Rapid", "Mon premier tournois")
result = tournament.save_on_db()

if result is True:
    player01 = Player("QUIROUL", "Pierre", "05/12/1980", "M")
    save_player(player01)
    tournament.add_player(player01.get_id)
    player02 = Player("BONOD", "Jean", "01/04/1902", "M")
    save_player(player02)
    tournament.add_player(player02.get_id)
    player03 = Player("IMAL", "Anne", "15/10/1986", "F")
    save_player(player03)
    tournament.add_player(player03.get_id)
    player04 = Player("HOL", "Lucie", "08/02/1945", "F")
    save_player(player04)
    tournament.add_player(player04.get_id)
    match1 = Match(player01, player02)
    match1.set_score(1, 0)
    match2 = Match(player03, player04)
    match2.set_score(0, 1)
    round1 = Round("Round-1")
    round1.add_match(match1)
    round1.add_match(match2)
    round1.set_end(time.time())
    tournament.update_round(round1)
    print(tournament)
else:
    print(f"Erreur le tournoi existe dèja, son id est: {result}")

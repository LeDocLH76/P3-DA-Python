from tinydb import TinyDB, Query, where
from models.player import Player

player_1 = Player("Joueur 1", "Prénom 1", "01/05/1996", "M")
player_2 = Player("Joueur 2", "Prénom 2", "15/01/1986", "M", 1)

# print(player_1.get_player)
# print(player_2.get_player)

db = TinyDB('chess_tournament')
# db.drop_tables()
players_table = db.table("players")

# insert un après l'autre
players_table.insert(player_1.get_player)
players_table.insert(player_2.get_player)

# insert en bloc une liste de plusieurs
# aucun contrôle des doublons
# players_table.insert_multiple(
#     [player_1.get_player, player_2.get_player])

# retourne une liste de ceux qui match
player = Query()
print(players_table.search(player.classification == 2))

# retourne le premier qui match et recupere sont id
player = players_table.get(where("classification") == 2)
print(player)
player_id = player.doc_id
print(player_id)


# met à jour ceux qui match
players_table.update({"points": 1},
                     (where("name") == "Joueur 1")
                     & (where("classification") == 2))

# Déja présent ???
if players_table.search(
    (player.name == "Joueur 1")
    & (player.surname == "Prénom 1")
        & (player.birth_date == "1996-05-01")):
    print("Cet enregistrement est déja présent en base!")

# retourne tous
print(players_table.all())

# boucle sur tous
for player in players_table:
    print(player)

import random
from typing import List

from tinydb import TinyDB
from models.player import Player
from models.match import Match
from models.round import Round
from models.tournament import Tournament

# Définition des huits joueurs

# Les 20 prénoms les plus portés en France chez les filles :
prenom_f = ["Marie", "Nathalie", "Isabelle", "Sylvie", "Catherine",
            "Françoise", "Monique", "Martine", "Christine", "Nicole",
            "Anne", "Valérie", "Jacqueline", "Sandrine", "Sophie",
            "Stéphanie", "Véronique", "Céline", "Chantal", "Patricia"]

# Les 20 prénoms les plus portés en France chez les garçons :
prenom_h = ["Jean", "Michel", "Philippe", "Pierre", "Alain",
            "Nicolas", "Christophe", "Patrick", "Christian", "Daniel",
            "Bernard", "David", "Frédéric", "Laurent", "Eric",
            "Julien", "Sébastien", "Stéphane", "Pascal", "Thomas"]

prenom = []
for pre_h in prenom_h:
    prenom.append(pre_h)
    prenom.append(prenom_f[prenom_h.index(pre_h)])

random.shuffle(prenom)
# print(prenom)

nom = ["Martin", "Bernard", "Thomas", "Petit", "Robert",
       "Richard", "Durand", "Dubois", "Moreau", "Laurent",
       "Simon", "Michel", "Lefebvre", "Leroy", "Roux",
       "David", "Bertrand", "Morel", "Fournier", "Girard"]

# nom = ["Martin", "Bernard", "Martin", "Bernard", "Martin",
#        "Bernard", "Martin", "Bernard", "Martin", "Bernard"]

random.shuffle(nom)
# print(nom)

date = []
for i in range(20):
    day = str(random.randrange(1, 30))
    month = str(random.randrange(1, 12))
    year = str(random.randrange(1922, 2014))
    date_to_add = f"{day}/{month}/{year}"
    date.append(date_to_add)

# print(date)


players_obj: List[Player] = []
for i in range(8):
    genre = "F" if prenom[i] in prenom_f else "M"
    player = Player(nom[i], prenom[i], date[i], genre, i+1)
    # print(players[i].get_player)
    players_obj.append(player)

# print(players_obj)

# ******************************
# Début tournois
# ******************************
# Ligne à supprimer !!!
#
db = TinyDB('chess_tournament')
db.drop_tables()
# ******************************

# Création du tournoi
tournament = Tournament("Tournoi privé", "Le Havre",
                        "11/10/2022", "rapid", "Mon premier tournoi d'échec")
tournament.save_db()
# Ajout des joueurs
for player in players_obj:
    tournament.add_player(player)
    player.save_db()

# Mélange des joueurs dans la liste
random.shuffle(players_obj)

# Création du 1er tour
round_1 = Round("Round 1")

# ******************************
# Début Systeme Suisse
# ******************************

# Trie la liste de Player par leur classification, ascendant
players_obj.sort(key=lambda x: x.get_player["classification"])
# Sépare la liste en 2 listes
list_1_length = len(players_obj)//2
list_1 = players_obj[:list_1_length]
list_2 = players_obj[list_1_length:]
# Si le nombre de joueurs est impair,
# le dernier ne peut-être apparié et reçois 1/2 point pour ne pas jouer
if len(list_2) > len(list_1):
    list_2[-1].add_point(0.5)

# Association des joueurs pour le round-1
matches_list: List[tuple[Player, Player]] = []
for i in range(len(list_1)):
    matches_list.append((list_1[i], list_2[i]))

# Création de la listes des instances de Match pour le round_1
round_1_matches_list: List[Match] = []

print("Les match du premier tour sont:")

for player_1, player_2 in matches_list:

    print(f"{player_1}\ncontre\n{player_2}\n")

    match = Match(player_1, player_2)
    round_1_matches_list.append(match)

# Ajoute les Match dans le round_1
for match in round_1_matches_list:
    round_1.add_match(match)

# Ajoute le Round au tournoi
tournament.add_round(round_1)
tournament.update_round_db

# ******************************
# Entrée des points par match pour round_1
# ******************************
score = [1.0, 0.5, 0.0]

print("Résultat du round-1")

for match in round_1_matches_list:
    score1 = random.choice(score)
    score2 = 1 - score1
    player_1: Player = match.get_players[0]
    player_2: Player = match.get_players[1]
    match.set_score(score1, score2)
    player_1.add_point(score1)
    player_1.update_points_db(score1)
    player_2.add_point(score2)
    player_2.update_points_db(score2)

    print(f"{player_1}\nNombre de points: \
{player_1.get_player['points']}")
    print(f"{player_2}\nNombre de points: \
{player_2.get_player['points']}")
    print()

tournament.update_round_db()
# ******************************
# Début du/des autres rounds
# ******************************
players_obj = tournament.get_players
# Trie les joueurs par points puis par classement si égalité de points
players_obj = sorted(players_obj, key=lambda x: x.get_player["classification"])
players_obj = sorted(
    players_obj, key=lambda x: x.get_player["points"], reverse=True)
for player in players_obj:
    print(player.get_player["name"], player.get_player["points"],
          player.get_player["classification"])

# Créé une liste des matchs interdit: si les joueurs se sont déja rencontrés
match_already_played = tournament.get_matchs_already_played
print()
# print(match_already_played[0].get_players[0])
# print(match_already_played[0].get_players[1])
forbiden_pairs: List[tuple[Player, Player]] = []
for match in match_already_played:
    pair = (match.get_players[0].get_player["name"],
            match.get_players[1].get_player["name"])
    forbiden_pairs.append(pair)
print("Associations interdites")
print(forbiden_pairs)
print()

# Stop
# Stop
# Stop
# Stop

players_free: List[list[Player, bool]] = []
for player in players_obj:
    player_to_add = [player, True]
    # print(player_to_add)
    players_free.append(player_to_add)
print()


def find_player_free(players_free: List[list[Player, bool]]):
    index = 0
    find = False
    while find is False or index < len(players_free):
        if players_free[i][1] is True:
            # print(players_free[i][0].get_player["name"])
            players_free[i][1] = False
            find = True
            return players_free[i]
        else:
            index += 1


odd_players_list = False
if len(players_free) % 2 != 0:
    odd_players_list = True


# # Compose les paires de joueurs pour le round
# pairs_player_list: List[tuple[Player, Player]] = []
# for i in range(0, len(players_obj), 2):
#     pair = (players_obj[i].get_player["name"],
#             players_obj[i+1].get_player["name"])
#     pairs_player_list.append(pair)
# print(pairs_player_list)
# print()

# # Recherche si les joueurs se sont déja rencontrés
# for pair in pairs_player_list:
#     for forbiden_pair in forbiden_pairs:
#         inverted_pair = (pair[1], pair[0])
#         if pair == forbiden_pair or inverted_pair == forbiden_pair:
#             print("Alerte, les joueurs se sont déja rencontrés!")

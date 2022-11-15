import random
import time
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


def create_players(players_quantity):
    from models.db_manager_players import Db_manager_player
    manager_player = Db_manager_player()
    # Création des joueurs
    players_obj: List[Player] = []
    for i in range(players_quantity):
        classification = random.randrange(1, 100)
        genre = "F" if prenom[i] in prenom_f else "M"
        player = Player(nom[i], prenom[i], date[i], genre, classification)
        reponse = manager_player.add_one(player)
        if reponse is not True:
            print("Le joueur existe déja")
            player.set_id(reponse)
        players_obj.append(player)
    return players_obj


db = TinyDB('chess_tournament')
# db.drop_tables()

# ******************************
# Début tournoi
# ******************************

# Création du tournoi
tournament = Tournament("Tournoi privé",
                        "Le Havre",
                        "05/11/2022",
                        "rapid",
                        "Mon cinquième tournoi d'échecs")

reponse = tournament.save_db()
if reponse is not True:
    print("Le tournoi existe déja")
    tournament.set_id(reponse)

players_obj = create_players(8)

# Ajout des id de joueurs dans le dictionnaire du tournoi
# cle = "id" valeur = points = 0
# et sauve sur la bd
for player in players_obj:
    tournament.add_player(player.get_id)

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
    tournament.update_player_point(list_2[-1].get_id, 0.5)

# Association des joueurs pour le round-1
matches_list: List[tuple[Player, Player]] = []
for i in range(len(list_1)):
    matches_list.append((list_1[i], list_2[i]))

# Création de la listes des instances de Match pour le round_1
round_x_matches_list: List[Match] = []

print()
print("Les match du premier tour sont:")

for player_1, player_2 in matches_list:

    print(f"{player_1}\ncontre\n{player_2}\n")

    match = Match(player_1, player_2)
    round_x_matches_list.append(match)

# Ajoute les Match dans le round_1
for match in round_x_matches_list:
    round_1.add_match(match)

# Fin du round
time.sleep(2)
round_1.set_end(time.time())
print(round_1)
print()

# Ajoute le Round au tournoi et sauve sur bd
tournament.update_round(round_1)

# ******************************
# Entrée des points par match pour round_1
# ******************************
score = [1.0, 0.5, 0.0]

print("Résultat du round-1")
print()

for match in round_x_matches_list:
    score1 = random.choice(score)
    score2 = 1 - score1
    player_1: Player = match.get_players[0]
    player_2: Player = match.get_players[1]
    match.set_score(score1, score2)
    tournament.update_player_point(player_1.get_id, score1)
    tournament.update_player_point(player_2.get_id, score2)

    print(f"{player_1}\nNombre de points: \
{tournament.get_points(player_1.get_id)}")
    print(f"{player_2}\nNombre de points: \
{tournament.get_points(player_2.get_id)}")
    print()
# Met à jour sur bd
tournament.update_round()
# ******************************
# Début du/des autres rounds
# ******************************

# Créé une liste des matchs interdit: si les joueurs se sont déja rencontrés
match_already_played = tournament.get_matchs_already_played
print()
# print(match_already_played[0].get_players[0])
# print(match_already_played[0].get_players[1])
forbiden_pairs: List[tuple[Player, Player]] = []
for match in match_already_played:
    # Crée un tuple d'instance de joueur s'étant déja rencontrés
    pair = (match.get_players[0],
            match.get_players[1])
    forbiden_pairs.append(pair)
# print("Associations interdites")
# print(forbiden_pairs)
# print()

# A ce stade:
# forbiden_pair est une liste de tuples d'instance de joueur
# s'étant déja rencontrés


def find_player_free(players_free: List[list[Player | bool]]) -> Player | None:
    index = 0
    find = False
    while find is False and index < len(players_free):
        if players_free[index][1] is True:
            players_free[index][1] = False
            find = True
            return players_free[index]
        else:
            index += 1
    return None

# ***********************
# ***********************
# ***********************


for round_x in range(3):
    print(f"début du round {round_x + 2}")

    # Créé un nouveau round
    round_x_obj = Round(f"Round_{round_x + 2}")

    # Crée un liste intermédiaire de joueurs et les rend libre pour appairage
    # Libre = True
    players_free = []
    for player in players_obj:
        player_to_add = [player, True]
        players_free.append(player_to_add)
    # print(f"Liste de joueurs libre {players_free}")

    # Trie les joueurs par points puis par classement si égalité de points
    players_obj = sorted(
        players_obj,
        key=lambda x: x.get_player["classification"])
    players_obj = sorted(
        players_obj,
        key=lambda x: tournament.get_points(x.get_id),
        reverse=True)
    print("Joueurs triés pour le prochain tour")
    for player in players_obj:
        print(player.get_player["name"], tournament.get_points(player.get_id),
              player.get_player["classification"])

    matches_list = []
    rejected_players = []
    time_ = 1

    while True:
        player_free = find_player_free(players_free)
        if time_ <= 2:
            if time_ == 1:
                if player_free is None:
                    break
                player_1 = player_free
                time_ = 2
            else:
                if player_free is None:
                    print(
                        f"Le joueur {player_1[0]} n'est pas associé, \
il faut lui donner 0.5 points")
                    player: Player = player_1[0]
                    tournament.update_player_point(player.get_id, 0.5)
                    # Sortie du while
                    break
                player_2 = player_free

                # Paire interdite ???
                if (((player_1[0], player_2[0]) in forbiden_pairs)
                        or
                        ((player_2[0], player_1[0]) in forbiden_pairs)):
                    print(f"Alerte association interdite \
{player_1[0]} {player_2[0]}")
                    rejected_players.append(player_free)
                    free_flag = False
                    # Cherche si il existe encore un joueur libre
                    for free_player in players_free:
                        if free_player[1] is True:
                            free_flag = True
                    # Si oui tente une autre association
                    if free_flag is True:
                        # Retour au while
                        continue
                    # Si non associe les 2 joueurs quand même
                    print(
                        "Association contrainte *************************")
                    # Sortir le joueur_2 des joueurs refusés
                    rejected_players = [
                        rejected_player for rejected_player
                        in rejected_players
                        if rejected_player != player_2]

                match = (player_1[0], player_2[0])
                matches_list.append(match)
                # Si des associations ont été refusées
                if len(rejected_players) > 0:
                    # On libére les joueurs refusés
                    for rejected_player in rejected_players:
                        index = players_free.index(rejected_player)
                        players_free[index][1] = True
                    # Et on vide la liste
                    rejected_players = []
                time_ = 1
                # print(match)
                # Retour au while
    # Ajoute les paires de ce tour à la liste des paires interdites
    forbiden_pairs.extend(matches_list)

# ***************
    # Faire jouer et entrer les resultats
    # Ajouter les matchs
    # Ajouter le round
    # Création de la listes des instances de Match pour le round_1
    round_x_matches_list: List[Match] = []
    print()
    print(f"Les match du tour {round_x_obj.get_name} sont:")
    print()

    for player_1, player_2 in matches_list:

        print(f"{player_1}\ncontre\n{player_2}\n")

        match = Match(player_1, player_2)
        round_x_matches_list.append(match)

    # Ajoute les Match dans le round_x
    for match in round_x_matches_list:
        round_x_obj.add_match(match)

    # Fin du round
    time.sleep(2)
    round_x_obj.set_end(time.time())
    print(round_x_obj)
    print()

    # Ajoute le Round au tournoi
    tournament.update_round(round_x_obj)

    # ******************************
    # Entrée des points par match pour round_x
    # ******************************
    score = [1.0, 0.5, 0.0]

    print(f"Résultat du round-{round_x_obj.get_name}")
    print()

    for match in round_x_matches_list:
        score1 = random.choice(score)
        score2 = 1 - score1
        player_1: Player = match.get_players[0]
        player_2: Player = match.get_players[1]
        match.set_score(score1, score2)
        tournament.update_player_point(player_1.get_id, score1)
        tournament.update_player_point(player_2.get_id, score2)

        print(f"{player_1}\nNombre de points: \
    {tournament.get_points(player_1.get_id)}")
        print(f"{player_2}\nNombre de points: \
    {tournament.get_points(player_2.get_id)}")
        print()

    tournament.update_round()

    # Boucle 3 fois

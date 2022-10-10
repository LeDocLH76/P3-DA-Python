from random import randrange, shuffle
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

shuffle(prenom)
# print(prenom)

nom = ["Martin", "Bernard", "Thomas", "Petit", "Robert",
       "Richard", "Durand", "Dubois", "Moreau", "Laurent",
       "Simon", "Michel", "Lefebvre", "Leroy", "Roux",
       "David", "Bertrand", "Morel", "Fournier", "Girard"]

shuffle(nom)
# print(nom)

date = []
for i in range(20):
    day = str(randrange(1, 30))
    month = str(randrange(1, 12))
    year = str(randrange(1922, 2014))
    date_to_add = f"{day}/{month}/{year}"
    date.append(date_to_add)

# print(date)

players = []
for i in range(20):
    player_to_add = "player_" + str(i+1)
    players.append(player_to_add)

# print(players)

players_obj = []
for i in range(8):
    genre = "F" if prenom[i] in prenom_f else "M"
    players[i] = Player(nom[i], prenom[i], date[i], genre, i+1)
    # print(players[i].get_player)
    players_obj.append(players[i])

# print(players_obj)

shuffle(players_obj)
for i in range(len(players_obj)):
    print(players_obj[i].get_player)


# ******************************
# Début Systeme Suisse
# ******************************

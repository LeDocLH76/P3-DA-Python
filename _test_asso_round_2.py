
import random
from typing import List

# Les joueurs sont classés par ordre points/classement
joueurs_libres: List[list] = [
    ["a", True],
    ["b", True],
    ["c", True],
    ["d", True],
    ["e", True],
    ["f", True],
    ["g", True],
    ["h", True],
    ["i", True]]

# Paires de joueurs interdite pour le tour2
asso_interdites = [
    ("a", "b"),
    ("g", "e"),
    ("d", "c"),
    ("f", "h")]


def find_player_free(
        joueurs_libres: list[list[str | bool]]) -> list[str | bool] | None:
    index = 0
    find = False
    while find is False and index < len(joueurs_libres):
        if joueurs_libres[index][1] is True:
            # print(joueurs_libres[index][0])
            joueurs_libres[index][1] = False
            find = True
            return joueurs_libres[index]
        else:
            index += 1
    return None


def main():
    for round in range(3):
        # Libère tous les joueurs
        for joueur in joueurs_libres:
            joueur[1] = True
        # Liste de paires pour ce round
        pairs = []
        # Simule un nouveau classement suite au round précedent
        random.shuffle(joueurs_libres)
        print(f"Round_{round + 1}")
        joueurs_refuse = []
        passage = 1
        while True:
            joueur = find_player_free(joueurs_libres)
            if passage <= 2:
                if passage == 1:
                    if joueur is None:
                        break
                    joueur_1 = joueur
                    passage = 2
                else:
                    if joueur is None:
                        print(
                            f"Le joueur {joueur_1[0]} n'est pas associé, \
il faut lui donner 0.5 points")
                        # Sortie du while
                        break
                    joueur_2 = joueur

                    # Paire interdite ???
                    if (((joueur_1[0], joueur_2[0]) in asso_interdites)
                            or ((joueur_2[0], joueur_1[0])
                                in asso_interdites)):
                        print(f"Alerte association interdite \
{joueur_1[0]} {joueur_2[0]}")
                        joueurs_refuse.append(joueur)
                        libre = False
                        # Cherche si il existe encore un joueur libre
                        for joueur_libre in joueurs_libres:
                            if joueur_libre[1] is True:
                                libre = True
                        # Si oui tente une autre association
                        if libre is True:
                            # Retour au while
                            continue
                        # Si non associe les 2 joueurs quand même
                        print(
                            "Association contrainte *************************")
                        # Sortir le joueur_2 des joueurs refusés
                        joueurs_refuse = [
                            joueur for joueur
                            in joueurs_refuse
                            if joueur != joueur_2]

                    pair = (joueur_1[0], joueur_2[0])
                    pairs.append(pair)
                    # Si des associations ont été refusées
                    if len(joueurs_refuse) > 0:
                        # On libére les joueurs refusés
                        for joueur in joueurs_refuse:
                            index = joueurs_libres.index(joueur)
                            joueurs_libres[index][1] = True
                        # Et on vide la liste
                        joueurs_refuse = []
                    passage = 1
                    print(pair)
                    # Retour au while
        # Ajoute les paires de ce tour à la liste des paires interdites
        asso_interdites.extend(pairs)
        # Boucle 3 fois


if __name__ == "__main__":
    main()

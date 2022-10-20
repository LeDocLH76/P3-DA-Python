
# Les joueurs sont classés par ordre points/classement
joueurs_libres = [
    ["a", True],
    ["b", True],
    ["c", True],
    ["d", True],
    ["e", True],
    ["f", True],
    ["g", True],
    ["h", True],
    ["i", True]]

# Paires de joueurs tour2
asso_interdites = [
    ("a", "b"),
    ("g", "e"),
    ("d", "c"),
    ("f", "h")]

# Paires de joueurs tour3
# asso_interdites = [
#     ("a", "b"),
#     ("g", "e"),
#     ("d", "c"),
#     ("f", "h"),
#     ("a", "c"),
#     ("b", "d"),
#     ("e", "f"),
#     ("g", "h")]

# Paires de joueurs tour4
# asso_interdites = [
#     ("a", "b"),
#     ("g", "e"),
#     ("d", "c"),
#     ("f", "h"),
#     ("a", "c"),
#     ("b", "d"),
#     ("e", "f"),
#     ("g", "h"),
#     ("a", "d"),
#     ("b", "c"),
#     ("e", "h"),
#     ("f", "g")]


asso_interdites = set(asso_interdites)

pairs = []


def find_player_free(joueurs_libres) -> list | None:
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
    joueurs_refuse = []
    passage = 1
    while True:
        joueur = find_player_free(joueurs_libres)
        if passage <= 2:
            if passage == 1:
                joueur_1 = joueur
                passage = 2
            else:
                if joueur is None:
                    print(
                        f"Le joueur {joueur_1[0]} n'est pas associé, \
il faut lui donner 0.5 points")
                    break
                joueur_2 = joueur

                # Interdit ???
                asso_ok = True
                if (joueur_1[0], joueur_2[0]) in asso_interdites:
                    asso_ok = False
                if (joueur_2[0], joueur_1[0]) in asso_interdites:
                    asso_ok = False

                if asso_ok is False:
                    print(f"Alerte association interdite \
{joueur_1[0]} {joueur_2[0]}")
                    joueurs_refuse.append(joueur)
                    # Si il existe encore un joueur libre
                    libre = False
                    for joueur_libre in joueurs_libres:
                        if joueur_libre[1] is True:
                            libre = True
                    # Tente une autre association
                    if libre is True:
                        continue
                    # Si non associe les 2 joueurs quand même
                pair = (joueur_1[0], joueur_2[0])
                pairs.append(pair)
                if len(joueurs_refuse) > 0:
                    for joueur in joueurs_refuse:
                        index = joueurs_libres.index(joueur)
                        joueurs_libres[index][1] = True
                    joueurs_refuse = []
                passage = 1
                print(pair)
    print(pairs)


if __name__ == "__main__":
    main()

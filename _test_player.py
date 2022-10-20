from models.player import Player

birth_date = ['13/8/2002', '11/11/2012', '24/2/2011']
joueur = Player("BONNOT", "Jean", birth_date[0], "M")
print(joueur.get_player)
print(joueur.get_player["name"])
print([key for key in joueur.get_player])
print([joueur.get_player[key] for key in joueur.get_player])
print(joueur)
joueur.set_classification(1)
print(joueur)


from views import views_input, views_output


def tournament_controler():
    # tournoi en cours   status = False
    # le nombre de round à jouer n'est pas atteint
    # un round n'est pas cloturés
    # tournoi cloturé    status = True
    # le nombre de round à jouer est atteint
    # tous les rounds sont cloturés

    # rounds en cours    valeur = 1 à max

    # round en cours     status = False
    # la liste de matchs n'est pas cloturée
    # round cloturé      status = True
    # la liste de matchs est cloturée

    # matchs en cours    status = False
    # les matchs ne sont pas tous renseignés
    # matchs cloturé     status = True
    # les matchs sont tous renseignés
    # l'utilisateur a validé la cloture

    ...
    # initialiser un tournoi ! déja créé ?
    # afficher les tournois existants
    views_output.tournament_list()
    # input créer un tournoi ou quitter
    # input les datas pour la création
    tournament_dict = views_input.new_tournament()
    views_output.tournament_data(tournament_dict)
    # changer le nombre de rounds ?

    # verifier si déja existant
    # controler sur la database
    # créer le tournoi
    # init
    # afficher le tournoi et sont status
    # nom date timeControl
    # roundsTerminés/nbrDeRounds
    # roundEnCours matchsRenseignés/matchsDuRound

    # ajouter des joueurs ! déja ajouté ?
    # afficher la liste des joueurs
    # demander quel joueur ajouter
    # afficher le menu input
    # le joueur est dans la liste -> le selectionner
    # le joueur n'est pas dans la liste -> le créer
    # afficher la liste des joueurs
    # tout les joueurs ont-il été ajoutés ?
    # verifier la quantité de joueurs et cloturer la création !!! irreverssible
    # mettre à jour le status du tournoi

    # initialiser un round ! quel round?
    # verifier le status du tournoi
    # verifier le status des rounds
    # verifier le nombre de rounds prévus
    # créer le round x
    # mettre à jour le status du round

    # créer les matchs ! quel round?
    # verifier le status des rounds
    # si round 1
    # appairer les joueurs par moitié
    # si non
    # appairer les joueurs suivant algo paires consecutives
    # afficher les matchs à jouer
    # mettre à jour le status du round

    # ... les joueurs jouent...

    # entrer le resultat d'un match ! quel round? quel match?
    # afficher les matchs du round en cours
    # input quel match renseigner ?
    # verifier si tous les matchs sont renseignés
    # afficher les matchs du round en cours
    # input demander cloturer le round

    # le round est-il terminé ?
    # le round est-il le dernier

    # le tournois est-il terminé ?

Pre-requis:
Python 3.10 compris pip

Créer le répertoire de l'application "mon_repertoire"
Se déplacer dans le repertoire créé
cd mon_repertoire
Avec Git:
Cloner le repos Git
git clone https://github.com/LeDocLH76/P3-DA-Python .
Sans Git:
Se rendre à l'adresse https://github.com/LeDocLH76/P3-DA-Python
Sous l'onglet <> Code
Download ZIP
Décompresser l'archive dans le repertoire "mon_repertoire"

Pour la première utilisation, suivre les étapes 1 à 5

1- Ouvrir un terminal de commande et se rendre dans le repertoire créé

2- Création de l'environnement:
python -m venv env

3- Activation de l'environnement:
env\Scripts\activate

4- Installation des dépendances:
python -m pip install -r requirements.txt

5- Lancement de l'application:
python -m main

Pour les lancement futur seul 1, 3 et 5 sont necessaires

Déactivation de l'environnement:
deactivate

Création du rapport flake8 HTML:
flake8 --config setup.cfg --format=html --htmldir=flake-report

Création du rapport flake8 TXT:
Seule les dernières lignes de ce très gros fichier sont interessantes.
flake8 -vv --extend-exclude env --output-file=flake-report\flake8_report.txt

Pour un test du programme uniquement:
Il est possible de créer une base de données remplie en executant le fichier populate.py
Si cette option est utilisée, il est nécessaire de supprimer le fichier chess_tournament après les tests.
Attention, ne jamais utiliser cette option si le programme à déja été utilisé en condition de tournoi réél, car des données parasites serai ajoutées sur la base de données.

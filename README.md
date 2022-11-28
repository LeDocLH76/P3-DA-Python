Création de l'environnement:
python -m venv env

Activation de l'environnement:
env\Scripts\activate

Installation des dépendances:
python -m pip install -r requirements.txt

Lancement de l'application:
python -m main

Création du rapport flake8 HTML:
flake8 --config setup.cfg --format=html --htmldir=flake-report

Déactivation de l'environnement:
deactivate

Création du rapport flake8 TXT:
Seule les dernières lignes de ce très gros fichier sont interessantes.
flake8 -vv --extend-exclude env --output-file=flake-report\flake8_report.txt

Création de l'environnement:
python -m venv env

Activation de l'environnement:
env\Scripts\activate

Installation des dépendances:
python -m pip install -r requirements.txt

Lancement de l'application:
python -m main

Déactivation de l'environnement:
deactivate

Création du rapport flake8:
flake8 --format=html --htmldir=flake-report --extend-exclude env

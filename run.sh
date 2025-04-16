#!/bin/bash
echo "Calculateur de Diffusion - Installation et Lancement"
echo "================================================"
echo

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "Python n'est pas installé ou n'est pas dans le PATH."
    echo "Veuillez installer Python depuis https://www.python.org/downloads/"
    exit 1
fi

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Erreur lors de la création de l'environnement virtuel."
        exit 1
    fi
fi

# Activer l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "Installation des dépendances..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Erreur lors de l'installation des dépendances."
    echo "Tentative d'installation sans version spécifique..."
    pip install Flask Flask-SQLAlchemy Flask-Login Flask-Mail Flask-Migrate Flask-WTF Werkzeug numpy python-dotenv email-validator SQLAlchemy alembic click itsdangerous Jinja2 Mako MarkupSafe
    if [ $? -ne 0 ]; then
        echo "Erreur lors de l'installation des dépendances sans version spécifique."
        exit 1
    fi
fi

# Initialiser la base de données
echo "Initialisation de la base de données..."
python -c "from app import create_app; app = create_app(); from extensions import db; app.app_context().push(); db.create_all()"
if [ $? -ne 0 ]; then
    echo "Erreur lors de l'initialisation de la base de données."
    exit 1
fi

# Lancer l'application
echo "Lancement de l'application..."
echo "L'application sera accessible à l'adresse: http://localhost:5000"
echo "Appuyez sur Ctrl+C pour arrêter l'application."
echo
python app.py

# Désactiver l'environnement virtuel
deactivate
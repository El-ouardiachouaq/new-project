@echo off
echo Calculateur de Diffusion - Installation et Lancement
echo ================================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo Python n'est pas installé ou n'est pas dans le PATH.
    echo Veuillez installer Python depuis https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Vérifier si l'environnement virtuel existe
if not exist venv (
    echo Création de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo Erreur lors de la création de l'environnement virtuel.
        pause
        exit /b 1
    )
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances
echo Installation des dépendances...
pip install -r requirements.txt
if errorlevel 1 (
    echo Erreur lors de l'installation des dépendances.
    echo Tentative d'installation sans version spécifique...
    pip install Flask Flask-SQLAlchemy Flask-Login Flask-Mail Flask-Migrate Flask-WTF Werkzeug numpy python-dotenv email-validator SQLAlchemy alembic click itsdangerous Jinja2 Mako MarkupSafe
    if errorlevel 1 (
        echo Erreur lors de l'installation des dépendances sans version spécifique.
        pause
        exit /b 1
    )
)

REM Initialiser la base de données
echo Initialisation de la base de données...
python -c "from app import create_app; app = create_app(); from extensions import db; app.app_context().push(); db.create_all()"
if errorlevel 1 (
    echo Erreur lors de l'initialisation de la base de données.
    pause
    exit /b 1
)

REM Lancer l'application
echo Lancement de l'application...
echo L'application sera accessible à l'adresse: http://localhost:5000
echo Appuyez sur Ctrl+C pour arrêter l'application.
echo.
python app.py

REM Désactiver l'environnement virtuel
call venv\Scripts\deactivate.bat

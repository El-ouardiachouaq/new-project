# Calculateur de Diffusion - Guide d'Installation

Ce guide vous aidera à installer et exécuter le Calculateur de Diffusion sur votre ordinateur.

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (optionnel, pour cloner le dépôt)

## Étapes d'Installation

### 1. Installation de Python

1. Téléchargez Python depuis [python.org](https://www.python.org/downloads/)
2. Lors de l'installation, cochez la case "Add Python to PATH"
3. Vérifiez l'installation en ouvrant un terminal (cmd) et en tapant:
   ```
   python --version
   ```

### 2. Configuration du Projet

1. Créez un dossier pour le projet:
   ```
   mkdir diffusion_calculator
   cd diffusion_calculator
   ```

2. Créez un environnement virtuel:
   ```
   python -m venv venv
   ```

3. Activez l'environnement virtuel:
   - Sur Windows:
     ```
     venv\Scripts\activate
     ```
   - Sur Linux/Mac:
     ```
     source venv/bin/activate
     ```

### 3. Installation des Dépendances

1. Installez les bibliothèques requises:
   ```
   pip install flask
   pip install flask-sqlalchemy
   pip install flask-login
   pip install flask-mail
   pip install numpy
   pip install python-dotenv
   pip install werkzeug
   ```

   Ou utilisez le fichier requirements.txt:
   ```
   pip install -r requirements.txt
   ```

### 4. Configuration de la Base de Données

1. Initialisez la base de données:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

### 5. Configuration des Variables d'Environnement

1. Créez un fichier `.env` à la racine du projet avec le contenu suivant:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=votre_clé_secrète
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=votre_email@gmail.com
   MAIL_PASSWORD=votre_mot_de_passe
   MAIL_DEFAULT_SENDER=votre_email@gmail.com
   ```

### 6. Lancement de l'Application

1. Démarrez l'application:
   ```
   flask run
   ```

2. Ouvrez votre navigateur et accédez à:
   ```
   http://localhost:5000
   ```

## Dépannage

### Problèmes Courants

1. **Erreur "ModuleNotFoundError"**
   - Solution: Réinstallez les dépendances:
     ```
     pip install -r requirements.txt
     ```

2. **Erreur de Base de Données**
   - Solution: Supprimez le dossier `migrations` et le fichier `instance/database.db`, puis réinitialisez:
     ```
     flask db init
     flask db migrate
     flask db upgrade
     ```

3. **Erreur de Port**
   - Solution: Changez le port dans la commande de lancement:
     ```
     flask run --port=5001
     ```

### Support

Pour toute question ou problème, contactez:
- Email: elouardiachouaq@gmail.com
- Développeur: EL-OUARDI ACHOUAQ

## Fonctionnalités

- Calcul des coefficients de diffusion
- Historique des calculs
- Interface utilisateur moderne
- Visualisation 3D des molécules
- Support multilingue (Français/Anglais) 
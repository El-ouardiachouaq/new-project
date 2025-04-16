#!/bin/bash
echo "Creating project structure..."
mkdir -p static/css
mkdir -p static/js
mkdir -p templates

echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install Flask==2.3.3 flask-sqlalchemy==3.1.1 numpy==1.24.3 Werkzeug==2.3.7
pip freeze > requirements.txt

echo "Setup complete! You can now run the application with ./run.sh"
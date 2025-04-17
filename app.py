from flask import Flask, render_template # type: ignore
from config import Config
from extensions import db, mail, login_manager
from flask_login import current_user # type: ignore
from dotenv import load_dotenv # type: ignore
import os

# Load environment variables from .env file
load_dotenv()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure SQLALCHEMY_DATABASE_URI is set
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("The 'SQLALCHEMY_DATABASE_URI' configuration is missing. Please set it in the environment or Config class.")

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from main import bp as main_bp
    app.register_blueprint(main_bp)

    from calculator import bp as calculator_bp
    app.register_blueprint(calculator_bp)

    # Register error handlers
    register_error_handlers(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', error='Page not found'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('error.html', error='Internal server error'), 500

if __name__ == '__main__':
    import sys
    import os
    # Print the Python executable path for debugging
    print(f"Using Python executable: {sys.executable}")
    # Print the environment variables for debugging
    print(f"Environment Variables: {os.environ}")
    # Relax the check to ensure the virtual environment is being used
    if "venv" not in sys.executable:
        raise RuntimeError("Incorrect Python executable. Please activate the virtual environment.")
    print(f"SQLALCHEMY_DATABASE_URI: {os.getenv('SQLALCHEMY_DATABASE_URI')}")
    app = create_app()
    app.run(debug=True)
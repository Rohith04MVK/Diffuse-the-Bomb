from flask import Flask
from .config import Config
from .extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints or routes here
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Register CLI commands
    from .models import User, Puzzle
    @app.cli.command("init-db")
    def init_db_command():
        """Clears existing data and creates new tables."""
        with app.app_context(): # Commands need the app context
            db.create_all()
        print("Initialized the database.")

    return app
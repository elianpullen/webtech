from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class) # Get config from config.py

    # Login manager
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    # Import and register blueprints
    from .admin import admin
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(admin, url_prefix='/admin')  # Admin routes

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
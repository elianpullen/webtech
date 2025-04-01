import os
from flask import Flask, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt
from models import db, Exercise
from routes import routes


app = Flask(__name__)

bcrypt = Bcrypt(app)

# Configure app settings
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mijngeheimesleutel')  # Use environment variable for SECRET_KEY
basedir = os.path.abspath(os.path.dirname(__file__))  # Get base directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')  # Set path to database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app) # Initialize database

routes(app) # import routes

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
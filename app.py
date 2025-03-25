from flask import Flask, render_template, request, redirect, url_for    
from models import db, Exercise
from routes import routes
import os

app = Flask(__name__)

# Configure the SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the base directory
instance_dir = os.path.join(BASE_DIR, 'instance')
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)

# Configure the database URI
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(instance_dir, 'database.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)  # Initialize db with app

routes(app) # import routes

# Create tables if necessary
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
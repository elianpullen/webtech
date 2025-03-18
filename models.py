from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    #duration = db.Column(db.Integer, nullable=True)
    #repetitions = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())  # Current timestamp using func.now()
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())  # Updated timestamp using func.now()

    # add constructor
    def __init__(self, name, description=None, category="General"):
        self.name = name
        self.description = description
        self.category = category
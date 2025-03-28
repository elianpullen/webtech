from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Integer, nullable=False, default=0)
    bodyweight = db.Column(db.Integer, nullable=True) 
    bodyfat = db.Column(db.Integer, nullable=True)

    def __init__(self, name, password, is_admin, bodyweight, bodyfat): # add constructor
        self.name = name
        self.password = password
        self.is_admin = is_admin
        self.bodyweight = bodyweight
        self.bodyfat = bodyfat

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    exercises = db.relationship('Exercise', back_populates='category')  # Relationship to Exercise

    def __init__(self, name): # add constructor
        self.name = name

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False) # Foreign Key to Category.id
    
    category = db.relationship('Category', back_populates='exercises')

    def __init__(self, name, description, category_id): # add constructor
        self.name = name
        self.description = description
        self.category_id = category_id
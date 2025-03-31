from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Integer, nullable=False, default=0)
    bodyweight = db.Column(db.Float, nullable=True) 
    bodyfat = db.Column(db.Float, nullable=True)

    workouts = db.relationship('Workout', back_populates='user', lazy=True)  # Relationship to Workout

    def __init__(self, name, password, bodyweight, bodyfat, is_admin=False): # add constructor
        self.name = name
        self.password = password
        self.is_admin = is_admin
        self.bodyweight = bodyweight
        self.bodyfat = bodyfat

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    exercises = db.relationship('Exercise', back_populates='category', lazy=True)  # Relationship to Exercise

    def __init__(self, name): # add constructor
        self.name = name

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False) # Foreign Key to Category.id
    
    category = db.relationship('Category', back_populates='exercises')

    def __init__(self, name, category_id, description=""): # add constructor
        self.name = name
        self.description = description
        self.category_id = category_id
        

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=False)
    reps = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Integer, nullable=True) 
    note = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Foreign Key to User.id

    user = db.relationship('User', back_populates='workouts')

    def __init__(self, name, reps, weight, duration, date, note, user_id): # add constructor
        self.name = name
        self.reps = reps
        self.weight = weight
        self.duration = duration
        self.date = date
        self.note = note
        self.user_id = user_id
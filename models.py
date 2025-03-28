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

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    #category
    reps = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    duration = db.Column(db.Interval, nullable=True)
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    note = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Foreign Key to User.id

    user = db.relationship('User', back_populates='workouts')

    def __init__(self, name, reps, weight, duration, note, user_id): # add constructor
        self.name = name
        self.reps = reps
        self.weight = weight
        self.duration = duration
        self.date = date
        self.note = note
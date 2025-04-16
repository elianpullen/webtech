from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .password_utils import PasswordMixin

class User(db.Model, UserMixin, PasswordMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    bodyweight = db.Column(db.Float, nullable=True)
    bodyfat = db.Column(db.Float, nullable=True)

    # db relationship to Workout model (one-to-many), only load workouts when accessed (lazy=True), delete workouts when user is deleted
    workouts = db.relationship('Workout', back_populates='user', lazy=True, cascade='all, delete-orphan') 

    # constructor so elements can be accessed
    def __init__(self, username, password, bodyweight=None, bodyfat=None, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.bodyweight = bodyweight
        self.bodyfat = bodyfat

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    # db relationship to Exercise model (one-to-many), only load exercise when accessed (lazy=True), delete exercises when category is deleted
    exercises = db.relationship('Exercise', back_populates='category', lazy=True, cascade='all, delete-orphan')

    # constructor so elements can be accessed
    def __init__(self, name):
        self.name = name

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False) # foreign key to Category model

    # db relationship to Category model (many-to-one), only load category when accessed (lazy=True)
    category = db.relationship('Category', back_populates='exercises')
    # db relationship to Workout_Exercise model (one-to-many), only load workout_exercises when accessed (lazy=True), delete workout_exercises when exercise is deleted
    workout_exercises = db.relationship('Workout_Exercise', back_populates='exercise', lazy=True, cascade='all, delete-orphan')

    # constructor so elements can be accessed
    def __init__(self, name, category_id, description=""):
        self.name = name
        self.description = description
        self.category_id = category_id

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    date = db.Column(db.Integer, nullable=True)
    note = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # foreign key to User model

    # db relationship to User model (many-to-one)
    user = db.relationship('User', back_populates='workouts')
    # db relationship to Workout_Exercise model (one-to-many), only load workout_exercises when accessed (lazy=True), delete workout_exercises when workout is deleted
    workout_exercises = db.relationship('Workout_Exercise', back_populates='workout', lazy=True, cascade='all, delete-orphan')

    # constructor so elements can be accessed
    def __init__(self, name, reps, weight, duration, date, note, user_id):
        self.name = name
        self.reps = reps
        self.weight = weight
        self.duration = duration
        self.date = date
        self.note = note
        self.user_id = user_id

class Workout_Exercise(db.Model):
    __tablename__ = 'workout_exercise'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)

    # db relationship to Workout model (many-to-one)
    workout = db.relationship('Workout', back_populates='workout_exercises')
    # db relationship to Exercise model (many-to-one)
    exercise = db.relationship('Exercise', back_populates='workout_exercises')
    # db relationship to ExerciseSet model (one-to-many), only load exercise_sets when accessed (lazy=True), delete exercise_sets when workout_exercise is deleted
    exercise_sets = db.relationship('ExerciseSet', back_populates='workout_exercise', lazy=True, cascade="all, delete-orphan")

    # constructor so elements can be accessed
    def __init__(self, workout_id, exercise_id):
        self.workout_id = workout_id
        self.exercise_id = exercise_id

class ExerciseSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_exercise_id = db.Column(db.Integer, db.ForeignKey('workout_exercise.id'), nullable=False) # foreign key to Workout_Exercise model
    set_number = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Float)
    duration = db.Column(db.Integer)

    # db relationship to Workout_Exercise model (many-to-one)
    workout_exercise = db.relationship('Workout_Exercise', back_populates='exercise_sets')

    # constructor so elements can be accessed
    def __init__(self, workout_exercise_id, set_number, reps, weight, duration):
        self.workout_exercise_id = workout_exercise_id
        self.set_number = set_number
        self.reps = reps
        self.weight = weight
        self.duration = duration

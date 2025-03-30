from models import db, User, Category, Exercise, Workout
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

with app.app_context():
    db.create_all()

    # Create User
    user1 = User(name='John Doe', password='password123', bodyweight=80.5, bodyfat=20.0)
    db.session.add(user1)

    # Create Category
    category1 = Category(name='Strength')
    db.session.add(category1)

    # Create Exercise
    exercise1 = Exercise(name='Bench Press', description='Chest exercise', category_id=1)
    exercise2 = Exercise(name='Squat', description='Leg exercise', category_id=1)
    db.session.add(exercise1)
    db.session.add(exercise2)

    # Create Workout
    workout1 = Workout(name='Full Body Workout', reps=10, weight=50.0, duration=60, note='Good session')

    db.session.add(workout1)

    db.session.commit()
    print('Database populated successfully!')

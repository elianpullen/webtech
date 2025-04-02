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
workout1 = Workout(name='Full Body Workout', reps=10, weight=50.0, duration=60, date=60, note='Good session', user_id=1)
db.session.add(workout1)
db.session.commit()
print('Database populated successfully!')
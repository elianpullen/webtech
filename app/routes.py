from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Exercise, Category, User, Workout, Workout_Exercise, ExerciseSet
from .forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():# Check if user already exists
            flash('Username already taken!', 'error')
            return redirect(url_for('main.register'))

        user = User(
            username=form.username.data,
            password=form.password.data
        )

        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        # Check user exists and password is correct
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!')
    return redirect(url_for('main.index'))

@main.route("/about/")
def about():
    return render_template("about.html")
    
@main.route('/workout/')
@login_required
def workout():
    workouts = Workout.query.filter_by(user_id=current_user.id).all()
    return render_template('workout/index.html', workouts=workouts)

@main.route('/workout/add/', methods=['GET', 'POST'])
@login_required
def add_workout():
    exercises = Exercise.query.all()

    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        note = request.form.get('note') or ""

        # Create the workout
        new_workout = Workout(
            name=name,
            date=date,
            note=note,
            user_id=current_user.id
        )
        db.session.add(new_workout)
        db.session.flush()  # Get new_workout.id before committing

        # Loop through form keys to find selected exercises
        for key in request.form:
            if key.startswith('exercise_') and request.form.get(key) == 'on':
                try:
                    exercise_id = int(key.split('_')[1])
                except (IndexError, ValueError):
                    continue  # skip malformed input just in case

                # Create association table entry
                workout_exercise = Workout_Exercise(
                    workout_id=new_workout.id,
                    exercise_id=exercise_id
                )
                db.session.add(workout_exercise)
                db.session.flush()

                # Get form data (may be empty depending on exercise type)
                reps_list = request.form.getlist(f'reps_{exercise_id}[]')
                weight_list = request.form.getlist(f'weight_{exercise_id}[]')
                duration_list = request.form.getlist(f'duration_{exercise_id}[]')

                # Determine the longest list to loop through
                max_len = max(len(reps_list), len(weight_list), len(duration_list))

                for i in range(max_len): # if i is out of range, it will be skipped
                    reps = int(reps_list[i]) if i < len(reps_list) and reps_list[i] else 0
                    weight = float(weight_list[i]) if i < len(weight_list) and weight_list[i] else 0.0
                    duration = int(duration_list[i]) if i < len(duration_list) and duration_list[i] else 0

                    set_entry = ExerciseSet(
                        workout_exercise_id=workout_exercise.id,
                        set_number=i + 1,
                        reps=reps,
                        weight=weight,
                        duration=duration
                    )
                    db.session.add(set_entry)

        db.session.commit()
        flash('Workout created successfully!', 'success')
        return redirect(url_for('main.workout'))

    return render_template('workout/add.html', exercises=exercises)

@main.route('/workout/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_workout(id):
    workout = Workout.query.get_or_404(id)
    
    # Check if the user is the owner of the workout
    if workout.user_id != current_user.id:
        return redirect(url_for('main.workout'))
    
    exercises = Exercise.query.all()
    
    # Create a dictionary to track which exercises are selected
    workout_exercises = {we.exercise_id: we for we in workout.workout_exercises}
    workout_sets = {}
    for we in workout.workout_exercises: # fetch all sets for this workout, ordered by set_number
        sets = ExerciseSet.query.filter_by(workout_exercise_id=we.id).order_by(ExerciseSet.set_number).all()
        workout_sets[we.exercise_id] = sets

    if request.method == 'POST':
        workout.name = request.form.get('name')
        workout.date = request.form.get('date')
        workout.note = request.form.get('note')
        
        # Delete all related ExerciseSets first
        for we in workout.workout_exercises:
            ExerciseSet.query.filter_by(workout_exercise_id=we.id).delete()

        # Then delete workout_exercises
        Workout_Exercise.query.filter_by(workout_id=workout.id).delete()
        
        db.session.flush()  # So we can re-use workout.id safely

        # Recreate all workout_exercises and sets
        for exercise in exercises:
            if request.form.get(f'exercise_{exercise.id}') == 'on':
                new_we = Workout_Exercise(workout_id=workout.id, exercise_id=exercise.id)
                db.session.add(new_we)
                db.session.flush()  # get new_we.id without committing

                for i in range(1, 5):  # Only allow up to 4 sets
                    reps = request.form.get(f'set_{exercise.id}_{i}_reps')
                    weight = request.form.get(f'set_{exercise.id}_{i}_weight')
                    duration = request.form.get(f'set_{exercise.id}_{i}_duration')
                
                    if reps or weight or duration:
                        new_set = ExerciseSet(
                            workout_exercise_id=new_we.id,
                            set_number=i,
                            reps=int(reps) if reps else 0,
                            weight=float(weight) if weight else 0,
                            duration=int(duration) if duration else 0
                        )
                        db.session.add(new_set)
                
        db.session.commit()
        flash('Workout updated successfully!', 'success')
        return redirect(url_for('main.workout'))
    
    return render_template('workout/edit.html', workout=workout, exercises=exercises, workout_exercises=workout_exercises, workout_sets=workout_sets)

@main.route('/workout/delete/<int:id>/', methods=['POST'])
@login_required
def delete_workout(id):
    workout = Workout.query.get_or_404(id)

    if workout.user_id != current_user.id: # Check if the user is the owner of the workout
        return redirect(url_for('main.workout'))

    db.session.delete(workout)
    db.session.commit()

    flash('Workout deleted successfully', 'success')
    return redirect(url_for('main.workout'))

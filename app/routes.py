from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Exercise, Category, User, Workout, Workout_Exercise
from .forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .utils import admin_required

main = Blueprint('main', __name__)

@main.route('/test')
def home():
    flash("This is a flash message!", "success")  # ("message", "category")
    return render_template('index.html')

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
            password=form.password.data  # Pass plaintext password
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

@main.route('/admin/')
@login_required
@admin_required
def admin():
    return render_template('admin/index.html')

@main.route('/admin/exercise/')
@login_required
@admin_required
def exercise():
    exercises = Exercise.query.all()
    return render_template('admin/exercise/index.html', exercises=exercises)

@main.route('/admin/exercise/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def add_exercise():
    categories = Category.query.all()
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category']
        description = request.form['description']
        new_exercise = Exercise(name=name, description=description, category_id=category_id)
        db.session.add(new_exercise)
        db.session.commit()
        return redirect(url_for('main.exercise'))
    return render_template('admin/exercise/add.html', categories=categories)

@main.route('/admin/exercise/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_exercise(id):
    categories = Category.query.all()
    exercise = Exercise.query.get_or_404(id)
    if request.method == 'POST':
        exercise.name = request.form.get('name')
        exercise.description = request.form.get('description')
        exercise.category_id = request.form.get('category_id')
        db.session.commit()
        return redirect(url_for('main.exercise'))
    return render_template('admin/exercise/edit.html', exercise=exercise, categories=categories)

@main.route('/admin/exercise/delete/<int:id>/', methods=['POST'])
@login_required
@admin_required
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return redirect(url_for('main.exercise'))

@main.route('/admin/user/')
@login_required
@admin_required
def user():
    users = User.query.all()
    return render_template("admin/user/index.html/", users=users)

@main.route('/admin/user/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin = request.form.get('is_admin') == 'on'
        bodyweight = request.form.get('bodyweight') or None
        bodyfat = request.form.get('bodyfat') or None
            
        new_user = User(username=username, password=password, is_admin=is_admin, bodyweight=bodyweight, bodyfat=bodyfat)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('main.user'))
    return render_template('/admin/user/add.html')

@main.route('/admin/user/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form.get('name')
        new_password = request.form.get('password')
        user.password = generate_password_hash(new_password)
        user.password = request.form.get('password')
        user.is_admin = request.form.get('is_admin') == 'on'
        user.bodyweight = request.form.get('bodyweight') or None
        user.bodyfat = request.form.get('bodyfat') or None
        db.session.commit()
        return redirect(url_for('main.user'))
    return render_template('/admin/user/edit.html', user=user)

@main.route('/admin/user/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('main.user'))

@main.route('/admin/category/')
@login_required
@admin_required
def category():
    categories = Category.query.all()
    return render_template("admin/category/index.html/", categories=categories)  

@main.route('/admin/category/add/', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
            
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        
        return redirect(url_for('main.category'))
    return render_template('/admin/category/add.html')

@main.route('/admin/category/edit/<int:id>/', methods=['GET', 'POST'])
def edit_category(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('name')
        category.name = name
        db.session.commit()

        return redirect(url_for('main.category'))
    return render_template('/admin/category/edit.html', category=category)

@main.route('/admin/category/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('main.category'))

@main.route("/about/")
def about():
    return render_template("about.html")
    
@main.route('/workout/')
@login_required
def workouts():
    workouts = Workout.query.filter_by(user_id=current_user.id).all()
    return render_template('workout/index.html', workouts=workouts)

@main.route('/workout/add/', methods=['GET', 'POST'])
@login_required
def add_workout():
    exercises = Exercise.query.all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        note = request.form.get('note')
        
        # Create the workout
        new_workout = Workout(
            name=name,
            reps=0,  # Default values
            weight=0,
            duration=0,
            date=date,
            note=note,
            user_id=current_user.id
        )
        db.session.add(new_workout)
        db.session.flush()
        
        # Process selected exercises
        for key, value in request.form.items():
            if key.startswith('exercise_'):
                exercise_id = int(key.split('_')[1])
                if value == 'on':  # Checkbox is checked
                    sets = request.form.get(f'sets_{exercise_id}') or 0
                    reps = request.form.get(f'reps_{exercise_id}') or 0
                    weight = request.form.get(f'weight_{exercise_id}') or 0
                    duration = request.form.get(f'duration_{exercise_id}') or 0
                    
                    workout_exercise = Workout_Exercise(
                        workout_id=new_workout.id,
                        exercise_id=exercise_id,
                        sets=sets,
                        reps=reps,
                        weight=weight,
                        duration=duration
                    )
                    db.session.add(workout_exercise)
        
        db.session.commit()
        flash('Workout created successfully!', 'success')
        return redirect(url_for('main.workouts'))
    
    return render_template('workout/add.html', exercises=exercises)

@main.route('/workout/delete/<int:id>/', methods=['POST'])
@login_required
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    
    # Check if the workout belongs to the current user
    if workout.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to delete this workout', 'danger')
        return redirect(url_for('main.workouts'))
    
    # Delete associated workout exercises first
    Workout_Exercise.query.filter_by(workout_id=id).delete()
    
    # Then delete the workout
    db.session.delete(workout)
    db.session.commit()
    
    flash('Workout deleted successfully', 'success')
    return redirect(url_for('main.workouts'))

@main.route('/workout/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_workout(id):
    workout = Workout.query.get_or_404(id)
    
    # Check if the workout belongs to the current user
    if workout.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to edit this workout', 'danger')
        return redirect(url_for('main.workouts'))
    
    exercises = Exercise.query.all()
    workout_exercises = {we.exercise_id: we for we in workout.workout_exercises}
    
    if request.method == 'POST':
        workout.name = request.form.get('name')
        workout.date = request.form.get('date')
        workout.note = request.form.get('note')
        
        # Delete existing workout exercises
        Workout_Exercise.query.filter_by(workout_id=id).delete()
        
        # Process selected exercises
        for key, value in request.form.items():
            if key.startswith('exercise_'):
                exercise_id = int(key.split('_')[1])
                if value == 'on':  # Checkbox is checked
                    sets = request.form.get(f'sets_{exercise_id}') or 0
                    reps = request.form.get(f'reps_{exercise_id}') or 0
                    weight = request.form.get(f'weight_{exercise_id}') or 0
                    duration = request.form.get(f'duration_{exercise_id}') or 0
                    
                    workout_exercise = Workout_Exercise(
                        workout_id=workout.id,
                        exercise_id=exercise_id,
                        sets=sets,
                        reps=reps,
                        weight=weight,
                        duration=duration
                    )
                    db.session.add(workout_exercise)
        
        db.session.commit()
        flash('Workout updated successfully!', 'success')
        return redirect(url_for('main.workouts'))
    
    return render_template('workout/edit.html', workout=workout, exercises=exercises, workout_exercises=workout_exercises)

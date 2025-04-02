from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Exercise, Category, User, Workout, Workout_Exercise
from .forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .utils import admin_required

main = Blueprint('main', __name__)

@main.route('/test')
def test():
    results = db.session.query(User, Workout).join(Workout).all()

    data = [
        {
            "user_id": user.id,
            "user_name": user.name,
            "workouts": user.workouts,
            #"workout_id": workout.id,
            #"activity": workout.activity,
            #"duration": workout.duration
        }
        for user, workout in results
    ]

    return render_template('test.html', data=data)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken!', 'error')
            return redirect(url_for('main.register'))

        # Create new user - let the User class handle password hashing
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
        user.password = request.form.get('password')
        user.is_admin = request.form.get('is_admin') == 'on'
        user.bodyweight = request.form.get('bodyweight') or None
        user.bodyfat = request.form.get('bodyfat') or None
        db.session.commit()
        return redirect(url_for('main.user'))
    return render_template('/admin/user/edit.html', user=user)

@main.route('/admin/user/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user_password(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        new_password = request.form.get('password')
            
        # Hash the new password before storing
        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Password updated successfully!', 'success')
        return redirect(url_for('main.user_profile', id=id))
        
    return render_template('/admin/user/edit_password.html', user=user)

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

@main.route('/log/', methods=['GET', 'POST'])
@login_required
def log():
    if request.method == 'POST':
        workout_type = request.form['workout_type']
        exercise = request.form.get('exercise', '')
        duration = request.form['duration']
        date = request.form['date']
        notes = request.form.get('notes', '')
        # Handle strength-specific fields
        reps = request.form.get('reps', None)
        weight = request.form.get('weight', None)
        # Process the data (e.g., save to a database)
        print(f"Workout logged: {workout_type}, {exercise}, {duration} minutes, {date}, Reps: {reps}, Weight: {weight}, Notes: {notes}")
        # Redirect to another page (e.g., progress page) after logging
        return redirect(url_for('main.index'))
    return render_template('log.html')
    
@main.route('/progress/', methods=['GET', 'POST'])
@login_required
def progress():
    # Example: Replace with actual database logic
    completed_workouts = 15  # Replace with a query to count completed workouts
    body_weight = 75  # Replace with the user's current weight from the database
    body_fat = 22  # Replace with the user's current body fat percentage from the database
    if request.method == 'POST':
        body_weight = request.form['body_weight']
        body_fat = request.form['body_fat']
        # Process the data (e.g., save to a database)
        print(f"Progress updated: Weight: {body_weight} kg, Body Fat: {body_fat}%")
        # Redirect to avoid form resubmission
        return redirect(url_for('main.progress'))
    return render_template('progress.html', completed_workouts=completed_workouts, body_weight=body_weight, body_fat=body_fat)
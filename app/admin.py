from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Exercise, Category, User, Workout, Workout_Exercise
from werkzeug.security import generate_password_hash
from .utils import admin_required
from flask_login import login_required, current_user

admin = Blueprint('admin', __name__)

def blueprint_admin_required():
    @admin.before_request
    @login_required
    def check_admin():
        if not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.index'))

blueprint_admin_required()

@admin.route('')
def index():
    return render_template('admin/index.html')

@admin.route('user/')
def user():
    users = User.query.all()
    return render_template("admin/user/index.html/", users=users)

@admin.route('user/add/', methods=['GET', 'POST'])
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
        
        return redirect(url_for('admin.user'))
    return render_template('admin/user/add.html')

@admin.route('user/edit/<int:id>/', methods=['GET', 'POST'])
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
        return redirect(url_for('admin.user'))
    return render_template('admin/user/edit.html', user=user)

@admin.route('user/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.user'))

@admin.route('exercise/')
def exercise():
    exercises = Exercise.query.all()
    return render_template('admin/exercise/index.html', exercises=exercises)

@admin.route('exercise/add/', methods=['GET', 'POST'])
def add_exercise():
    categories = Category.query.all()
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category']
        description = request.form['description'] or ""
        new_exercise = Exercise(name=name, description=description, category_id=category_id)
        db.session.add(new_exercise)
        db.session.commit()
        return redirect(url_for('admin.exercise'))
    return render_template('admin/exercise/add.html', categories=categories)

@admin.route('exercise/edit/<int:id>/', methods=['GET', 'POST'])
def edit_exercise(id):
    categories = Category.query.all()
    exercise = Exercise.query.get_or_404(id)
    if request.method == 'POST':
        exercise.name = request.form.get('name')
        exercise.description = request.form.get('description') or ""
        exercise.category_id = request.form.get('category_id')
        db.session.commit()
        return redirect(url_for('admin.exercise'))
    return render_template('admin/exercise/edit.html', exercise=exercise, categories=categories)

@admin.route('exercise/delete/<int:id>/', methods=['POST'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return redirect(url_for('admin.exercise'))

@admin.route('category/')
def category():
    categories = Category.query.all()
    return render_template("admin/category/index.html/", categories=categories)  

@admin.route('category/add/', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
            
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        
        return redirect(url_for('admin.category'))
    return render_template('admin/category/add.html')

@admin.route('category/edit/<int:id>/', methods=['GET', 'POST'])
def edit_category(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('name')
        category.name = name
        db.session.commit()

        return redirect(url_for('admin.category'))
    return render_template('admin/category/edit.html', category=category)

@admin.route('category/delete/<int:id>', methods=['POST'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('admin.category'))
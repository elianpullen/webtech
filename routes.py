from flask import render_template, request, redirect, url_for
from models import db, Exercise, Category

def routes(app):
    @app.route("/")
    def index():
        return render_template("index.html", name="Henk")

    @app.route('/admin/exercise/')
    def exercise():
        exercises = Exercise.query.all()
        return render_template('admin/exercise/index.html', exercises=exercises)

    @app.route('/admin/exercise/edit/<int:id>/', methods=['GET', 'POST'])
    def edit_exercise(id):
        categories = Category.query.all()
        exercise = Exercise.query.get_or_404(id)
        if request.method == 'POST':
            exercise.name = request.form['name']
            exercise.description = request.form['description']
            exercise.category = request.form['category']
            db.session.commit()
            return redirect(url_for('exercise'))
        return render_template('admin/exercise/edit.html', exercise=exercise, categories=categories)

    @app.route('/admin/exercise/add/', methods=['GET', 'POST'])
    def add_exercise():
        categories = Category.query.all()
        if request.method == 'POST':
            name = request.form['name']
            category_id = request.form['category']
            description = request.form['description']
            new_exercise = Exercise(name=name, description=description, category_id=category_id)
            db.session.add(new_exercise)
            db.session.commit()
            return redirect(url_for('exercise'))
        return render_template('admin/exercise/add.html', categories=categories)

    @app.route('/admin/exercise/delete/<int:id>/', methods=['POST'])
    def delete_exercise(id):
        exercise = Exercise.query.get_or_404(id)
        db.session.delete(exercise)
        db.session.commit()
        return redirect(url_for('exercise'))
    
    @app.route("/goals/")
    def goals():
        return render_template("goals.html")

    @app.route("/about/")
    def about():
        return render_template("about.html")

    @app.route('/log/', methods=['GET', 'POST'])
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
            return redirect(url_for('index'))

        return render_template('log.html')

    @app.route('/progress/', methods=['GET', 'POST'])
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
            return redirect(url_for('progress'))

        return render_template('progress.html', completed_workouts=completed_workouts, body_weight=body_weight, body_fat=body_fat)

from flask import render_template, request, redirect, url_for
from models import db, Exercise

# Define the route registration function
def init_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html", name="Henk")

    @app.route('/exercise')
    def exercise():
        exercises = Exercise.query.all()
        return render_template('admin/exercise/index.html', exercises=exercises)

    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit_exercise(id):
        exercise = Exercise.query.get_or_404(id)
        if request.method == 'POST':
            exercise.name = request.form['name']
            db.session.commit()
            return redirect(url_for('exercise'))
        return render_template('admin/exercise/edit.html', exercise=exercise)

    @app.route('/exercise/add', methods=['GET', 'POST'])
    def add_exercise():
        if request.method == 'POST':
            name = request.form['name']
            new_exercise = Exercise(name=name)
            db.session.add(new_exercise)
            db.session.commit()
            return redirect(url_for('exercise'))
        return render_template('admin/exercise/add.html')

    @app.route('/exercise/delete/<int:id>', methods=['POST'])
    def delete_exercise(id):
        exercise = Exercise.query.get_or_404(id)
        db.session.delete(exercise)
        db.session.commit()
        return redirect(url_for('exercise'))

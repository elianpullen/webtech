from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure the SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the base directory
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app)

# Create a simple model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@app.route("/")
def index():
    return render_template("index.html", name="Henk")

@app.route("/goals")
def goals():
    return render_template("goals.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/log', methods=['GET', 'POST'])
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

@app.route("/progress")
def progress():
    return render_template("progress.html")

if __name__ == "__main__":
    # Create the database file if it doesn't exist
    with app.app_context():
        db.create_all()
        print("Database created successfully!")
    
    app.run(debug=True)
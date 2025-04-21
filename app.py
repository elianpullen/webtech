import getpass
from app import db, create_app
from app.models import User, Category, Exercise
from werkzeug.security import generate_password_hash

class DatabaseInitializer:
    """Class to handle database initialization and admin user creation."""

    def __init__(self):
        """Initialize the class with the app context."""
        self.app = create_app()

    def create_tables(self):
        """Create all database tables."""
        with self.app.app_context():
            db.create_all()
            print("Database tables checked/created successfully!")

    def create_admin(self):
        """Create a default admin user if one doesn't exist."""
        with self.app.app_context():
            admin = User.query.filter_by(username='admin').first()
            
            if not admin:
                password = getpass.getpass("Enterr password for admin: ")

                default_admin = User(
                    username='admin',
                    password=password,
                    is_admin=1,
                )

                db.session.add(default_admin)
                db.session.commit()
                print("Default admin-account created!")
            else:
                print("Admin-account already exists! No changes made.")
    
    def create_default_categories(self):
        """Create default categories if they don't exist."""
        with self.app.app_context():
            category_names = ['Cardio', 'Fitness']

            for name in category_names:
                existing_category = Category.query.filter_by(name=name).first()
                if not existing_category:
                    new_category = Category(name=name)
                    db.session.add(new_category)
                    print(f"{name} Category created!")
                else:
                    print(f"Default {name} category already exists! No changes made.")
        
            db.session.commit()

    def create_default_exercises(self):
        """Create default exercises if they don't exist."""
        with self.app.app_context():
            # Define exercises with their category IDs
            exercises = [
                ('Bench Press', 2),   # Fitness
                ('Back squat', 2),    # Fitness
                ('Deadlift', 2),      # Fitness
                ('Stairmaster', 1),   # Cardio
                ('Running', 1),       # Cardio
            ]

            for name, category_id in exercises:
                existing_exercise = Exercise.query.filter_by(name=name).first()
                if not existing_exercise:
                    new_exercise = Exercise(name=name, category_id=category_id)
                    db.session.add(new_exercise)
                    print(f"{name} Exercise created!")
                else:
                    print(f"Default {name} exercise already exists! No changes made.")

            db.session.commit()

    def initialize_database(self):
        """Run all database initialization steps."""
        self.create_tables()
        self.create_admin()
        self.create_default_categories()
        self.create_default_exercises()

if __name__ == "__main__": # Only run this if this file is being run directly
    initializer = DatabaseInitializer()# Initialize database first
    initializer.initialize_database()
    
    app = create_app() # start flask app
    app.run(debug=True)
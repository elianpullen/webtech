import getpass
from app import db, create_app
from app.models import User
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
                password = getpass.getpass("Voer een wachtwoord in voor het admin-account: ")
                hashed_password = generate_password_hash(password)

                default_admin = User(
                    username='admin',
                    password=hashed_password,
                    is_admin=1,
                )

                db.session.add(default_admin)
                db.session.commit()
                print("Standaard admin-account aangemaakt!")
            else:
                print("Admin-account bestaat al! Geen wijzigingen aangebracht.")

    def initialize_database(self):
        """Run all database initialization steps."""
        self.create_tables()
        self.create_admin()

if __name__ == "__main__": # Only run this if this file is being run directly
    initializer = DatabaseInitializer()# Initialize database first
    initializer.initialize_database()
    
    app = create_app() # start flask app
    app.run(debug=True)
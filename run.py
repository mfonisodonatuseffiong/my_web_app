import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from flask_migrate import Migrate, upgrade
from app import create_app, db

# Ensure the application can find the 'app' module
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Create the Flask application instance
app = create_app()

# Set up Flask-Migrate
migrate = Migrate(app, db)

# Configure logging
if not app.debug:
    # File handler for production
    file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    app.logger.addHandler(file_handler)
else:
    # Console handler for development
    app.logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    app.logger.addHandler(handler)

@app.shell_context_processor
def make_shell_context():
    from app.models import User
    return {'db': db, 'User': User}

def init_db():
    """Initialize the database with migrations."""
    with app.app_context():
        # Apply migrations to the database
        upgrade()
        print("Database has been migrated and is up to date.")
        app.logger.info("Database has been migrated and is up to date.")

if __name__ == '__main__':
    # Uncomment the following line if you want to initialize the database
    # init_db()
    
    # Start the Flask application
    app.run(debug=True)

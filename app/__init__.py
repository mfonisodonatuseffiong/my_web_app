from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
# csrf = CSRFProtect()  # CSRFProtect initialization is commented out

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    # csrf.init_app(app)  # CSRFProtect initialization is commented out

    # Register blueprints
    from .routes import main
    app.register_blueprint(main, url_prefix='/')  # Register blueprint with a URL prefix if needed

    # Import models
    from .models import User

    # User loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

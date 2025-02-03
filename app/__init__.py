from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints
    from app.main.routes import main
    from app.auth.routes import auth
    
    app.register_blueprint(main)
    app.register_blueprint(auth)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app




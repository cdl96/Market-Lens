from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.config import Config
import google.generativeai as genai

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

    # Initialize Gemini
    if app.config.get('GOOGLE_API_KEY'):
        try:
            genai.configure(api_key=app.config['GOOGLE_API_KEY'])
            app.logger.info("Gemini API initialized successfully")
        except Exception as e:
            app.logger.error(f"Failed to initialize Gemini API: {e}")

    # Import and register blueprints
    from app.main.routes import main
    from app.auth.routes import auth
    
    app.register_blueprint(main)
    app.register_blueprint(auth)

    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating database tables: {e}")

    return app

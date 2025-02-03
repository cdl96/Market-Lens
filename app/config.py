import os
from datetime import timedelta

class Config:
    # Generate a secure secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'  # In production, use environment variable
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///market_lens.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    
    # Other configurations
    DEBUG = True  # Set to False in production
    WTF_CSRF_ENABLED = True


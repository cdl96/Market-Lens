import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI and '?' in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('?', '%3F')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')

    # Gemini configuration
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
    @staticmethod
    def init_gemini():
        if Config.GOOGLE_API_KEY:
            genai.configure(api_key=Config.GOOGLE_API_KEY)
            return genai.GenerativeModel('gemini-pro')
        else:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")



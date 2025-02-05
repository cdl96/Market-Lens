import google.generativeai as genai
from flask import current_app
from app import db
from app.models import Message, User

class AIService:
    def __init__(self):
        self.model = None
        self.ai_user = None
        self.initialize_ai()

    def initialize_ai(self):
        try:
            api_key = current_app.config['GOOGLE_API_KEY']
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            
            # Create or get AI user
            self.ai_user = User.query.filter_by(username='AI Assistant').first()
            if not self.ai_user:
                self.ai_user = User(
                    username='AI Assistant',
                    email='ai@assistant.com',
                    password='not_accessible'
                )
                db.session.add(self.ai_user)
                db.session.commit()
                
        except Exception as e:
            current_app.logger.error(f"Failed to initialize AI service: {e}")
            self.model = None

    async def process_message(self, user_message, user_id):
        if not self.model:
            return None

        try:
            # Generate AI response
            response = self.model.generate_content(user_message)
            
            # Create and save AI message
            ai_message = Message(
                sender_id=self.ai_user.id,
                receiver_id=user_id,
                content=response.text,
                is_ai_message=True
            )
            db.session.add(ai_message)
            db.session.commit()
            
            return ai_message
            
        except Exception as e:
            current_app.logger.error(f"Error processing AI message: {e}")
            return None

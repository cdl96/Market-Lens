import google.generativeai as genai

class AIService:
    def __init__(self, app=None):
        self.model = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        try:
            api_key = app.config['GOOGLE_API_KEY']
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            app.logger.error(f"Failed to initialize AI service: {e}")
            self.model = None

    async def get_response(self, user_message):
        """
        Simply get a response from Gemini AI for the given message
        """
        if not self.model:
            return "AI service is not properly initialized."

        try:
            response = self.model.generate_content(user_message)
            return response.text
        except Exception as e:
            print(f"Error getting AI response: {e}")
            return f"Error processing message: {str(e)}"

    async def analyze_sentiment(self, text):
        """
        Analyze the sentiment of given text
        """
        if not self.model:
            return "AI service is not properly initialized."

        prompt = f"""
        Analyze the sentiment of the following text and categorize it as POSITIVE, NEGATIVE, or NEUTRAL. 
        Also provide a confidence score between 0 and 1.
        Return the result in this format: SENTIMENT|SCORE
        
        Text to analyze: {text}
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return "NEUTRAL|0.0"

    async def summarize_text(self, text):
        """
        Generate a concise summary of the given text
        """
        if not self.model:
            return "AI service is not properly initialized."

        prompt = f"""
        Please provide a concise summary of the following text in 2-3 sentences:

        {text}
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"Error generating summary: {str(e)}"

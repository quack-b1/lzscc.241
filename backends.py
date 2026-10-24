import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

class GeminiBackend:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.model_name = model_name
        # automatically checks os.environ["GEMINI_API_KEY"]
        self.client = genai.Client()

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            return f"Error: {str(e)}"
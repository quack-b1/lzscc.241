import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

class GeminiBackend:
    def __init__(self, model_name="gemini-3.8-flash"):
        self.model_name = model_name
        # Explicitly pull the key from environment variables
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables or .env file.")

        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            return f"Error: {str(e)}"
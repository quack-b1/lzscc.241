import os
from dotenv import load_dotenv
from google import genai
from config import SELECTED_MODEL

load_dotenv()


class GeminiBackend:
    def __init__(self, model_name=SELECTED_MODEL):
        self.model_name = model_name
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
            if response and response.text:
                return response.text.strip()
            return "Error: Empty response received."
        except Exception as e:
            return f"Error: {str(e)}"
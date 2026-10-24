import os
from google import genai

class GeminiBackend:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.model_name = model_name
        # Automatically loads GEMINI_API_KEY from environment variables
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
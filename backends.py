import os
from dotenv import load_dotenv
from config import PROVIDER, SELECTED_MODEL

load_dotenv()


class ModelBackend:
    def __init__(self, model_name=SELECTED_MODEL, provider=PROVIDER):
        self.model_name = model_name
        self.provider = provider.lower()

        if self.provider == "gemini":
            from google import genai
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in .env file.")
            self.client = genai.Client(api_key=api_key)

        elif self.provider == "deepseek":
            from openai import OpenAI
            api_key = os.getenv("DEEPSEEK_API_KEY")
            if not api_key:
                raise ValueError("DEEPSEEK_API_KEY not found in .env file.")
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def generate(self, prompt: str) -> str:
        try:
            if self.provider == "gemini":
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )
                if response and response.text:
                    return response.text.strip()
                return "Error: Empty response received."

            elif self.provider == "deepseek":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    stream=False
                )
                return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Error: {str(e)}"
from openai import OpenAI
from core.config_loader import load_config

class OpenAIWrapper:
    def __init__(self):
        config = load_config()
        self.client = OpenAI(api_key=config["api"]["openai_api_key"])

    def get_completion(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
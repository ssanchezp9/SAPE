import os
from dotenv import load_dotenv

class EnvConfig:
    """Utility loader for environment variables."""

    def __init__(self):
        load_dotenv()

    def get_open_api_key(self) -> str:
        return os.getenv("OPENAI_API_KEY", "")

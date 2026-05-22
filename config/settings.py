import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


DEVELOPMENT_MODE = os.getenv(
    "DEVELOPMENT_MODE",
    "True"
).lower() == "true"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
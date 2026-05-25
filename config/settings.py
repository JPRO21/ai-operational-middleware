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

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

DAILY_BUDGET_USD = float(os.getenv("DAILY_BUDGET_USD", "1.0"))

LLM_RUNTIME_MODE = os.getenv("LLM_RUNTIME_MODE", "PRODUCTION").upper()

OPENAI_PRICING = {
    "gpt-4.1-mini": {
        "input": 0.0000004,
        "output": 0.0000016,
    }
}
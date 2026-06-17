from dotenv import load_dotenv
from pathlib import Path
import os

# Locate project root (two levels up from this file: app/config.py -> project root)
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


class Settings:
    MONGODB_URI = os.getenv("MONGODB_URI")

    DATABASE_NAME = os.getenv("DATABASE_NAME")

    APP_ENV = os.getenv("APP_ENV")

    MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", 10))

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


settings = Settings()


# Debug: warn if critical env vars are missing
if not settings.MONGODB_URI:
    print(f"WARNING: MONGODB_URI not set. Looked for .env at: {ENV_PATH}")

if not settings.DATABASE_NAME:
    print(f"WARNING: DATABASE_NAME not set. Looked for .env at: {ENV_PATH}")

if not settings.GEMINI_API_KEY:
    print(f"WARNING: GEMINI_API_KEY not set. Looked for .env at: {ENV_PATH}")

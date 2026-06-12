from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    MONGODB_URI = os.getenv("MONGODB_URI")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    APP_ENV = os.getenv("APP_ENV")
    MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", 10))

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


settings = Settings()

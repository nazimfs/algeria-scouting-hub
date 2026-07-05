import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

API_FOOTBALL_CONFIG = {
    "base_url": os.getenv("API_FOOTBALL_BASE_URL"),
    "api_key": os.getenv("API_FOOTBALL_KEY"),
}
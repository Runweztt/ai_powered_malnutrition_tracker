import os
from dotenv import load_dotenv

load_dotenv()  # reads the .env file

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
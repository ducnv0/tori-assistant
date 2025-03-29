import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///./test.db')
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')

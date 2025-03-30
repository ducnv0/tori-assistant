import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///./test.db')
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')
    WS_MAX_CONNECTIONS_PER_USER = int(os.getenv('WS_MAX_CONNECTIONS_PER_USER', 1))
    WS_PERIODICALLY_UPDATE_LAST_ACTIVE = int(
        os.getenv('WS_PERIODICALLY_UPDATE_LAST_ACTIVE', 10)
    )
    WS_STALE_CONNECTION_THRESHOLD = int(os.getenv('WS_STALE_CONNECTION_THRESHOLD', 20))
    WS_PERIODICALLY_CLEAN_STALE_CONNECTIONS = int(
        os.getenv('WS_PERIODICALLY_CLEAN_STALE_CONNECTIONS', 5)
    )
    WS_MAX_SIMULTANEOUS_USERS = int(os.getenv('WS_MAX_SIMULTANEOUS_USERS', 50))

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
    WS_CHECK_TIMEZONE_CONSTRAINT = bool(
        int(os.getenv('WS_CHECK_TIMEZONE_CONSTRAINT', '0'))
    )
    MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
    MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME', '')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', '')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', '')
    MINIO_SECURE = bool(int(os.getenv('MINIO_SECURE', '0')))
    MINIO_PRESIGNED_URL_EXPIRES_IN_SECONDS = int(
        os.getenv('MINIO_PRESIGNED_URL_EXPIRES_IN_SECONDS', 3600)
    )
    EXAMPLE_IMAGE = 'static/example_image.jpg'
    EXAMPLE_VIDEO = 'static/example_video.mp4'
    EXAMPLE_AUDIO = 'static/example_audio.mp3'

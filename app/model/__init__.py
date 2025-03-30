from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.model.base import Base
from app.model.conversation import Conversation
from app.model.message import Message
from app.model.user import User
from app.model.websocket_connection import WebsocketConnection
from config import Config


class Database:
    def __init__(self):
        self.async_engine = create_async_engine(
            Config.DATABASE_URL,
            echo=False,
            future=True,
            connect_args={"uri": True},  # Ensures the same database is used
        )

        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.async_engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def get_db(self):
        async with self.AsyncSessionLocal() as session:
            yield session


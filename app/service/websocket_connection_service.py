import asyncio
import datetime
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.exception import NotFoundError
from app.model.websocket_connection import WebsocketConnection
from app.repository.websocket_connection_repository import WebsocketConnectionRepository
from config import Config


class WebsocketConnectionService:
    def __init__(self, websocket_connection_repository: WebsocketConnectionRepository):
        self.websocket_connection_repository = websocket_connection_repository

    async def acquire_new_connection(
        self, db: AsyncSession, user_id: int, conversation_id: int
    ) -> bool:
        """
        1 connection / user / conversation
        Config.WS_MAX_CONNECTIONS_PER_USER / user
        Config.WS_MAX_SIMULTANEOUS_USERS / all users
        """
        # FIXME: Could race condition if two requests are made at the same time, should add lock for user_id

        # 1 connection / user / conversation
        connection = await self.websocket_connection_repository.find_by_user_id_and_conversation_id(
            db, user_id=user_id, conversation_id=conversation_id
        )
        if connection:
            return False

        # Config.WS_MAX_CONNECTIONS_PER_USER / user
        connection_count = (
            await self.websocket_connection_repository.count_connections_by_user(
                db, user_id=user_id
            )
        )
        if connection_count >= Config.WS_MAX_CONNECTIONS_PER_USER:
            return False

        # Config.WS_MAX_SIMULTANEOUS_USERS / all users
        connected_users_count = (
            await self.websocket_connection_repository.count_connected_users(db)
        )
        if connected_users_count >= Config.WS_MAX_SIMULTANEOUS_USERS:
            return False

        connection = WebsocketConnection(
            user_id=user_id,
            conversation_id=conversation_id,
            last_active=datetime.datetime.now(datetime.UTC),
        )
        await self.websocket_connection_repository.create(db, connection)
        logging.debug(
            'Websocket connection acquired for user_id %s and conversation_id %s',
            user_id,
            conversation_id,
        )
        return True

    async def release_connection(
        self, db: AsyncSession, user_id: int, conversation_id: int
    ) -> bool:
        connection = await self.websocket_connection_repository.find_by_user_id_and_conversation_id(
            db,
            user_id=user_id,
            conversation_id=conversation_id,
        )
        if connection:
            await self.websocket_connection_repository.delete(db, connection)
            logging.debug(
                'Websocket connection released for user_id %s and conversation_id %s',
                user_id,
                conversation_id,
            )
            return True
        return False

    async def update_last_active(
        self, db: AsyncSession, user_id: int, conversation_id: int
    ):
        connection = await self.websocket_connection_repository.find_by_user_id_and_conversation_id(
            db,
            user_id=user_id,
            conversation_id=conversation_id,
        )
        if not connection:
            raise NotFoundError(
                f'Websocket connection of user_id {user_id} and conversation_id {conversation_id} not found'
            )
        connection.last_active = datetime.datetime.now(datetime.UTC)
        await self.websocket_connection_repository.update(db, connection)

    async def periodically_update_last_active(
        self, db: AsyncSession, user_id: int, conversation_id: int
    ):
        while True:
            await asyncio.sleep(
                Config.WS_PERIODICALLY_UPDATE_LAST_ACTIVE
            )  # Update every 30 seconds
            await self.update_last_active(
                db,
                user_id=user_id,
                conversation_id=conversation_id,
            )
            logging.debug(
                'Websocket connection last active updated for user_id %s and conversation_id %s',
                user_id,
                conversation_id,
            )

    async def clean_stale_connections(self, db: AsyncSession):
        """
        Remove connections that have been inactive for a certain period.
        """
        last_active_before = datetime.datetime.now(datetime.UTC) - datetime.timedelta(
            seconds=Config.WS_STALE_CONNECTION_THRESHOLD
        )
        stale_connections = await self.websocket_connection_repository.search(
            db, last_active_to=last_active_before
        )
        for connection in stale_connections:
            await self.websocket_connection_repository.delete(db, connection)
        logging.info('Cleaned up %d stale connections', len(stale_connections))

    async def periodically_clean_stale_connections(self, db: AsyncSession):
        while True:
            await asyncio.sleep(Config.WS_PERIODICALLY_UPDATE_LAST_ACTIVE)
            await self.clean_stale_connections(db)

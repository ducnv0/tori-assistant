import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.websocket_connection import WebsocketConnection


class WebsocketConnectionRepository:
    async def find_by_user_id_and_conversation_id(
        self, db: AsyncSession, user_id: int, conversation_id: int
    ) -> WebsocketConnection | None:
        stmt = select(WebsocketConnection).where(
            WebsocketConnection.user_id == user_id,
            WebsocketConnection.conversation_id == conversation_id,
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self, db: AsyncSession, websocket_connection: WebsocketConnection
    ) -> WebsocketConnection:
        db.add(websocket_connection)
        await db.commit()
        await db.refresh(websocket_connection)
        return websocket_connection

    async def update(
        self, db: AsyncSession, websocket_connection: WebsocketConnection
    ) -> WebsocketConnection:
        await db.commit()
        await db.refresh(websocket_connection)
        return websocket_connection

    async def delete(
        self, db: AsyncSession, websocket_connection: WebsocketConnection
    ) -> None:
        await db.delete(websocket_connection)
        await db.commit()

    async def count_connections_by_user(self, db: AsyncSession, user_id: int) -> int:
        total_stmt = (
            select(func.count())
            .select_from(WebsocketConnection)
            .where(WebsocketConnection.user_id == user_id)
        )
        total_result = await db.execute(total_stmt)
        total_count = total_result.scalar()
        return total_count

    async def count_connected_users(self, db: AsyncSession) -> int:
        total_stmt = select(func.count(func.distinct(WebsocketConnection.user_id)))
        total_result = await db.execute(total_stmt)
        total_count = total_result.scalar()
        return total_count

    async def search(
        self,
        db: AsyncSession,
        last_active_to: datetime.datetime,
    ) -> list[WebsocketConnection]:
        filters = [WebsocketConnection.last_active <= last_active_to]

        stmt = select(WebsocketConnection).where(*filters)
        results = await db.execute(stmt)
        connections = results.scalars().all()
        return connections

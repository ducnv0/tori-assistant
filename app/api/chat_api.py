from fastapi import APIRouter, Depends, Query, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from app.injector import container

chat_router = APIRouter(tags=['Chat'])


@chat_router.websocket('/chat')
async def websocket_endpoint(
    websocket: WebSocket,
    conversation_id: int = Query(...),
    db: AsyncSession = Depends(container.database().get_db),
):
    await container.chat_service().handle_chat(
        db, conversation_id=conversation_id, websocket=websocket
    )

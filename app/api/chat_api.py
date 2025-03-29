from fastapi import APIRouter, WebSocket

from app.injector import container

chat_router = APIRouter(tags=['Chat'])


@chat_router.websocket('/chat')
async def websocket_endpoint(websocket: WebSocket):
    await container.chat_service().handle_chat(websocket)

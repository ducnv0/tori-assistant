import logging

from starlette.websockets import WebSocket, WebSocketDisconnect

from app.constant import WSReceiveType
from app.service.conversation_service import ConversationService
from app.service.user_service import UserService


class ChatService:
    def __init__(
        self, user_service: UserService, conversation_service: ConversationService
    ):
        self.user_service = user_service
        self.conversation_service = conversation_service

    async def handle_chat(self, websocket: WebSocket):
        await websocket.accept()
        logging.info('Client connected')

        try:
            while True:
                try:
                    data = await websocket.receive()
                    ws_receive_type = data.get('type', '')
                    if ws_receive_type == WSReceiveType.DISCONNECT:
                        raise WebSocketDisconnect

                    if 'text' in data:
                        logging.debug('Received text: %s', data['text'])
                        await websocket.send_text(f"Server received: {data['text']}")

                    elif 'bytes' in data:
                        logging.debug(
                            'Received binary data, length: %d', len(data['bytes'])
                        )
                        await websocket.send_text(
                            f"Received {len(data['bytes'])} bytes of binary data"
                        )
                except RuntimeError as e:
                    logging.error('RuntimeError: %s', e)
                    break
        except WebSocketDisconnect:
            logging.debug('WebSocket connection closed by client')
        finally:
            try:
                await websocket.close()
                logging.info('WebSocket connection closed')
            except RuntimeError as e:
                if (
                    str(e)
                    == "Unexpected ASGI message 'websocket.close', after sending 'websocket.close' or response already completed."
                ):
                    logging.debug(
                        'Cannot send websocket.close, WebSocket already closed'
                    )
                else:
                    logging.error('Error closing WebSocket: %s', e)

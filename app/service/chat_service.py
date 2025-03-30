import asyncio  # Add this import
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.constant import WSDataType, WSReceiveType
from app.schema.chat_schema import ReceiveMessage
from app.service.conversation_service import ConversationService
from app.service.user_service import UserService
from app.service.websocket_connection_service import WebsocketConnectionService


class ChatService:
    def __init__(
        self,
        user_service: UserService,
        conversation_service: ConversationService,
        websocket_connection_service: WebsocketConnectionService,
    ):
        self.user_service = user_service
        self.conversation_service = conversation_service
        self.websocket_connection_service = websocket_connection_service

    async def handle_chat(
        self, db: AsyncSession, conversation_id: int, websocket: WebSocket
    ):
        conversation = None
        can_connect = None
        update_last_active_task = None
        try:
            # Ensure the conversation exists
            conversation = await self.conversation_service.find_by_id(
                db, conversation_id
            )

            # Verify Config.WS_MAX_CONNECTIONS_PER_USER
            can_connect = (
                await self.websocket_connection_service.acquire_new_connection(
                    db, user_id=conversation.user_id, conversation_id=conversation.id
                )
            )
            if not can_connect:
                raise WebSocketDisconnect(
                    reason='User has reached the maximum number of connections'
                )

            await websocket.accept()
            logging.info('Client connected')

            # Periodically update last active
            update_last_active_task = asyncio.create_task(
                self.websocket_connection_service.periodically_update_last_active(
                    db,
                    user_id=conversation.user_id,
                    conversation_id=conversation.id,
                )
            )

            timezone = None
            while True:
                try:
                    data = await websocket.receive()
                    receive_message = ReceiveMessage.model_validate(data)
                    if receive_message.type == WSReceiveType.DISCONNECT:
                        raise WebSocketDisconnect
                    elif receive_message.type == WSReceiveType.RECEIVE:
                        if receive_message.data_type == WSDataType.TEXT_MESSAGE:
                            logging.debug(
                                'Received text: %s', receive_message.text_message
                            )
                            await websocket.send_text(
                                f'Server received: {receive_message.text_message}'
                            )
                        elif receive_message.data_type == WSDataType.BYTES_MESSAGE:
                            logging.debug(
                                'Received binary data, length: %d',
                                len(receive_message.bytes_message),
                            )
                            await websocket.send_text(
                                f'Received {len(receive_message.bytes_message)} bytes of binary data'
                            )
                        elif receive_message.data_type == WSDataType.TIMEZONE:
                            logging.debug(
                                'Received timezone: %s', receive_message.timezone
                            )
                            timezone = receive_message.timezone
                            # TODO: validate timezone?
                except RuntimeError as e:
                    logging.error('RuntimeError: %s', e)
                    break
        except WebSocketDisconnect:
            logging.debug('WebSocket connection closed by client')
        finally:
            if update_last_active_task:
                update_last_active_task.cancel()

            try:
                if can_connect and conversation:
                    await self.websocket_connection_service.release_connection(
                        db,
                        user_id=conversation.user_id,
                        conversation_id=conversation.id,
                    )
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

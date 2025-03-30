import asyncio  # Add this import
import datetime
import logging

import pytz
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.constant import WSDataType, WSReceiveType
from app.schema.chat_schema import ReceiveMessage
from app.service.conversation_service import ConversationService
from app.service.user_service import UserService
from app.service.websocket_connection_service import WebsocketConnectionService
from config import Config


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

            # Check connection constraints
            # 1 connection / user / conversation
            # Config.WS_MAX_CONNECTIONS_PER_USER / user
            # Config.WS_MAX_SIMULTANEOUS_USERS / all users
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
                        if receive_message.data_type == WSDataType.TIMEZONE:
                            logging.debug(
                                'Received timezone: %s', receive_message.timezone
                            )
                            timezone = receive_message.timezone
                            # TODO: validate timezone?

                        if receive_message.need_to_process:
                            # Check timezone constraints
                            if Config.WS_CHECK_TIMEZONE_CONSTRAINT:
                                if not await self.check_time_constraints(
                                    websocket=websocket,
                                    message_data_type=receive_message.data_type,
                                    timezone=timezone,
                                ):
                                    continue

                            # Process the message
                            if receive_message.data_type == WSDataType.TEXT_MESSAGE:
                                logging.debug(
                                    'Received text: %s', receive_message.text_message
                                )
                                await websocket.send_text(
                                    f'Server received: {receive_message.text_message}'
                                )
                            elif receive_message.data_type in [
                                WSDataType.AUDIO_MESSAGE,
                                WSDataType.VIDEO_MESSAGE,
                                WSDataType.IMAGE_MESSAGE,
                            ]:
                                len_bytes = len(
                                    receive_message.audio_message
                                    or receive_message.video_message
                                    or receive_message.image_message
                                )
                                logging.debug(
                                    'Received %s data, length: %d',
                                    receive_message.data_type,
                                    len_bytes,
                                )
                                await websocket.send_text(
                                    f'Received {len_bytes} bytes of {receive_message.data_type} data'
                                )

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

    async def check_time_constraints(
        self,
        websocket: WebSocket,
        message_data_type: WSDataType,
        timezone: str,
    ) -> bool:
        """
        Text chat: Accept if between 5 am and midnight.
        Video chat: Accept if between 8 pm and midnight.
        Voice chat: Accept if between 8 am and 12 pm.
        """
        if not timezone:
            await websocket.send_text('Timezone is required')
            return False
        timezone = pytz.timezone(timezone)
        now = datetime.datetime.now(timezone)
        if message_data_type == WSDataType.TEXT_MESSAGE:
            if now.hour < 5:
                await websocket.send_text(
                    'Text chat is only allowed between 5 am and midnight'
                )
                return False
        elif message_data_type in [WSDataType.VIDEO_MESSAGE, WSDataType.AUDIO_MESSAGE]:
            if now.hour < 20:
                await websocket.send_text(
                    'Video/Image chat is only allowed between 8 pm and midnight'
                )
                return False
        elif message_data_type == WSDataType.AUDIO_MESSAGE:
            if now.hour < 8 or now.hour > 12:
                await websocket.send_text(
                    'Voice chat is only allowed between 8 am and 12 pm'
                )
                return False
        return True

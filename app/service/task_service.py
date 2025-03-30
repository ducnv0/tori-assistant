import asyncio
import random

from sqlalchemy.ext.asyncio import AsyncSession

from app.constant import MessageType, Role
from app.service.message_service import MessageService
from config import Config


class TaskService:
    def __init__(self, message_service: MessageService):
        self.message_service = message_service
        self._init_example_data()

    def _init_example_data(self):
        with open(Config.EXAMPLE_AUDIO, 'rb') as f:
            self.audio_data = f.read()
        with open(Config.EXAMPLE_VIDEO, 'rb') as f:
            self.video_data = f.read()
        with open(Config.EXAMPLE_IMAGE, 'rb') as f:
            self.image_data = f.read()

    async def process_message(self, db: AsyncSession, message_id: int) -> list[int]:
        """
        Outsource the task to celery
        Celery gets the conversation history from database then call the LLM API
        Then save the response message to the database
        Then return the response message ids to the websocket

        Constraints:
        - Text chat: Reply with 1 text message. The response time could be randomized in [0,1] second.
        - Voice chat: Reply with 1 text message and 1 voice message. The response time
        could be randomized in [1,2] seconds
        - Video/Image chat: Reply with 1 text message, 1 voice message, and 1 image
        message. The response time could be randomized in [2,3] seconds
        """
        # TODO: Implement this method
        # MOCK
        message = await self.message_service.find_by_id(db, message_id)
        if message.role == Role.BOT:
            return []
        if message.message_type == MessageType.TEXT:
            await asyncio.sleep(random.uniform(0, 1))
            response_message = await self.message_service.create_text_message(
                db,
                conversation_id=message.conversation_id,
                role=Role.BOT,
                content=f'response for {message.content}',
            )
            return [response_message.id]
        elif message.message_type == MessageType.AUDIO:
            await asyncio.sleep(random.uniform(1, 2))
            response_message = await self.message_service.create_text_message(
                db,
                conversation_id=message.conversation_id,
                role=Role.BOT,
                content='response for audio type',
            )
            response_voice_message = await self.message_service.create_file_message(
                db,
                conversation_id=message.conversation_id,
                role=Role.BOT,
                data=self.audio_data,
                message_type=MessageType.AUDIO,
                content_type='audio/mpeg',
            )
            return [response_message.id, response_voice_message.id]
        elif message.message_type in [MessageType.VIDEO, MessageType.IMAGE]:
            await asyncio.sleep(random.uniform(2, 3))
            response_message = await self.message_service.create_text_message(
                db,
                conversation_id=message.conversation_id,
                role=Role.BOT,
                content='response for video/image type',
            )
            response_voice_message = await self.message_service.create_file_message(
                db,
                conversation_id=message.conversation_id,
                role=Role.BOT,
                data=self.audio_data,
                message_type=MessageType.AUDIO,
                content_type='audio/mpeg',
            )
            response_image_message = await self.message_service.create_file_message(
                db,
                conversation_id=message.conversation_id,
                role=Role.BOT,
                data=self.image_data,
                message_type=MessageType.IMAGE,
                content_type='image/jpeg',
            )
            return [
                response_message.id,
                response_voice_message.id,
                response_image_message.id,
            ]
        else:
            raise ValueError(f'Invalid message type: {message.message_type}')

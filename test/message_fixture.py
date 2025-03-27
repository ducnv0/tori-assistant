import pytest

from app.constant import MessageType, Role
from app.injector import container
from app.schema.message_schema import MessageCreateRequest
from test.conversation_fixture import ConversationFixture


class MessageFixture(ConversationFixture):
    @pytest.fixture
    async def message_1_user_text(self, conversation_1):
        async with container.database().AsyncSessionLocal() as db:
            return await container.message_service().create(
                db=db,
                req=MessageCreateRequest(
                    conversation_id=conversation_1.id,
                    role=Role.USER,
                    message_type=MessageType.TEXT,
                    content='Message 1 User Text',
                ),
            )

    @pytest.fixture
    async def message_2_bot_text(self, conversation_1):
        async with container.database().AsyncSessionLocal() as db:
            return await container.message_service().create(
                db=db,
                req=MessageCreateRequest(
                    conversation_id=conversation_1.id,
                    role=Role.BOT,
                    message_type=MessageType.TEXT,
                    content='Message 2 Bot Text',
                ),
            )

    @pytest.fixture
    async def message_3_user_audio(self, conversation_1):
        async with container.database().AsyncSessionLocal() as db:
            return await container.message_service().create(
                db=db,
                req=MessageCreateRequest(
                    conversation_id=conversation_1.id,
                    role=Role.USER,
                    message_type=MessageType.AUDIO,
                    file_path='s3-bucket/abc-123-audio.mp3',
                ),
            )

    @pytest.fixture
    async def message_4_user_image(self, conversation_2):
        async with container.database().AsyncSessionLocal() as db:
            return await container.message_service().create(
                db=db,
                req=MessageCreateRequest(
                    conversation_id=conversation_2.id,
                    role=Role.USER,
                    message_type=MessageType.IMAGE,
                    file_path='s3-bucket/abc-123-image.png',
                ),
            )

import pytest

from app.injector import container
from app.schema.conversation_schema import ConversationCreateRequest
from test.user_fixture import UserFixture


class ConversationFixture(UserFixture):
    @pytest.fixture
    async def conversation_1(self, user_1):
        async with container.database().AsyncSessionLocal() as db:
            return await container.conversation_service().create(
                db=db,
                req=ConversationCreateRequest(user_id=user_1.id, title='conversation_1'),
            )

    @pytest.fixture
    async def conversation_2(self, user_2):
        async with container.database().AsyncSessionLocal() as db:
            return await container.conversation_service().create(
                db=db,
                req=ConversationCreateRequest(user_id=user_2.id, title='conversation_2'),
            )

    @pytest.fixture
    async def conversation_3(self, user_1):
        async with container.database().AsyncSessionLocal() as db:
            return await container.conversation_service().create(
                db=db,
                req=ConversationCreateRequest(user_id=user_1.id, title='conversation_3'),
            )

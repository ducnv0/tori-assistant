import pytest

from app.injector import container
from app.schema.user_schema import UserCreateRequest


class UserFixture:

    @pytest.fixture
    async def user_1(self):
        async with container.database().AsyncSessionLocal() as db:
            return await container.user_service().create(
                db=db,
                req=UserCreateRequest(username='user_1'),
            )

    @pytest.fixture
    async def user_2(self):
        async with container.database().AsyncSessionLocal() as db:
            return await container.user_service().create(
                db=db,
                req=UserCreateRequest(username='user_2'),
            )

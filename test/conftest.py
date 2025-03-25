from config import Config

Config.DATABASE_URL = 'sqlite+aiosqlite:///:memory:'
from app.injector import container
from app.model import Base

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    client = TestClient(app)
    return client


@pytest.fixture(autouse=True)  # run for each test
async def setup_db():
    async with container.database().async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with container.database().async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

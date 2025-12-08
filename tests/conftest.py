from typing import (
    AsyncGenerator,
)

import pytest
import pytest_asyncio
from fakeredis.aioredis import FakeRedis
from httpx import (
    ASGITransport,
    AsyncClient,
)

from app.book.schemes import ContactData
from app.db.redis_conn import get_redis
from app.main import app


@pytest.fixture(scope="session")
def fake_redis() -> FakeRedis:
    """Create async FakeRedis."""
    redis = FakeRedis(
        decode_responses=True,
    )
    return redis


@pytest_asyncio.fixture
async def clean_redis(fake_redis: FakeRedis) -> FakeRedis:
    """Drop data in FakeRedis."""
    await fake_redis.flushall()
    return fake_redis


@pytest_asyncio.fixture
async def client(
    fake_redis: FakeRedis,
) -> AsyncGenerator[AsyncClient, None]:
    """Redefine client behavior for tests"""
    app.dependency_overrides[get_redis] = lambda: fake_redis
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def contact_data() -> ContactData:
    return ContactData(
        phone="74951001010",
        phone_normalized="+7(495)100-10-10",
        wrong_phone="+7(495)000-00-00",
        address="Test Address",
        extra_address="Extra Address",
    )

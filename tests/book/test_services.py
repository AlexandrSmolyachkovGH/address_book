import pytest
from fakeredis.aioredis import FakeRedis

from app.book.schemes import ContactData
from app.book.services import book_service
from app.custom_exceptions.custom_exceptions import (
    ServiceError,
)


@pytest.mark.asyncio
async def test_create_contact_data(
    fake_redis: FakeRedis,
    contact_data: ContactData,
    clean_redis: FakeRedis,
) -> None:
    created_data = await book_service.create_contact_data(
        phone=contact_data.phone_normalized,
        address=contact_data.address,
        redis_db=fake_redis,
    )

    assert created_data["phone"] == contact_data.phone_normalized
    assert created_data["address"] == contact_data.address


@pytest.mark.asyncio
async def test_get_contact_data(
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    get_data = await book_service.get_contact_data(
        phone=contact_data.phone,
        redis_db=fake_redis,
    )

    assert get_data["phone"] == contact_data.phone_normalized
    assert get_data["address"] == contact_data.address


@pytest.mark.asyncio
async def test_get_wrong_contact_data(
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    with pytest.raises(ServiceError) as exc_info:
        await book_service.get_contact_data(
            phone=contact_data.wrong_phone,
            redis_db=fake_redis,
        )

    assert "The address cannot be found" in str(exc_info.value)


@pytest.mark.asyncio
async def test_update_contact(
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    update_data = await book_service.update_contact(
        phone=contact_data.phone_normalized,
        new_address=contact_data.extra_address,
        redis_db=fake_redis,
    )

    assert update_data["phone"] == contact_data.phone_normalized
    assert update_data["address"] == contact_data.extra_address


@pytest.mark.asyncio
async def test_update_wrong_contact(
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    with pytest.raises(ServiceError) as exc_info:
        await book_service.update_contact(
            phone=contact_data.wrong_phone,
            new_address=contact_data.extra_address,
            redis_db=fake_redis,
        )

    assert str(exc_info.value) == "Phone doesn't exists"


@pytest.mark.asyncio
async def test_delete_contact(
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    deleted_data = await book_service.delete_contact(
        phone=contact_data.phone_normalized,
        redis_db=fake_redis,
    )

    assert deleted_data == contact_data.phone_normalized


@pytest.mark.asyncio
async def test_delete_wrong_contact(
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    with pytest.raises(ServiceError) as exc_info:
        await book_service.delete_contact(
            phone=contact_data.wrong_phone,
            redis_db=fake_redis,
        )

    assert str(exc_info.value) == "Phone doesn't exists"

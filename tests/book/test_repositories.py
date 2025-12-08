import pytest
from fakeredis.aioredis import FakeRedis

from app.book.repositories import book_repo
from app.book.schemes import ContactData


@pytest.mark.asyncio
async def test_create_record(
    fake_redis: FakeRedis,
    contact_data: ContactData,
    clean_redis: FakeRedis,
) -> None:
    created_data = await book_repo.create_record(
        phone=contact_data.phone_normalized,
        address=contact_data.address,
        redis_db=fake_redis,
    )

    assert created_data["phone"] == contact_data.phone_normalized
    assert created_data["address"] == contact_data.address


@pytest.mark.asyncio
async def test_get_address_by_phone(
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    address = await book_repo.get_address_by_phone(
        phone=contact_data.phone_normalized,
        redis_db=fake_redis,
    )

    assert address == contact_data.address


@pytest.mark.asyncio
async def test_check_conflict_number(
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    check_res = await book_repo.check_conflict_number(
        phone=contact_data.phone_normalized,
        redis_db=fake_redis,
    )

    assert check_res is True


@pytest.mark.asyncio
async def test_update_contact(
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    address = await book_repo.update_contact(
        phone=contact_data.phone_normalized,
        new_address=contact_data.extra_address,
        redis_db=fake_redis,
    )

    assert address["address"] == contact_data.extra_address


@pytest.mark.asyncio
async def test_delete_record(
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    delete_record = await book_repo.delete_record(
        phone=contact_data.phone_normalized,
        redis_db=fake_redis,
    )

    assert delete_record == 1

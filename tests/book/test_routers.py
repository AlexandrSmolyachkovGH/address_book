import pytest
from fakeredis.aioredis import FakeRedis
from httpx import (
    AsyncClient,
)

from app.book.schemes import (
    ContactData,
    CreateBookData,
    PhoneData,
    UpdateBookData,
)


@pytest.mark.asyncio
async def test_create_contact_data(
    client: AsyncClient,
    fake_redis: FakeRedis,
    contact_data: ContactData,
    clean_redis: FakeRedis,
) -> None:
    payload = CreateBookData(
        phone=contact_data.phone,
        address=contact_data.address,
    )

    response = await client.post(
        "/book/",
        json=payload.model_dump(),
    )

    data = response.json()
    assert response.status_code == 201
    assert data["phone"] == contact_data.phone_normalized
    assert data["address"] == contact_data.address


@pytest.mark.asyncio
async def test_create_repetitive_contact_data(
    client: AsyncClient,
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    repetitive_phone_payload = CreateBookData(
        phone=contact_data.phone,
        address=contact_data.address,
    )

    response = await client.post(
        "/book/",
        json=repetitive_phone_payload.model_dump(),
    )

    data = response.json()
    assert response.status_code == 409
    assert data["detail"] == "Phone already exists"


@pytest.mark.asyncio
async def test_get_contact_data(
    client: AsyncClient,
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    test_phone = PhoneData(
        phone=contact_data.phone,
    )

    response = await client.get(
        f"/book/{test_phone.phone}",
    )

    data = response.json()
    assert response.status_code == 200
    assert data["phone"] == contact_data.phone_normalized
    assert data["address"] == contact_data.address


@pytest.mark.asyncio
async def test_get_wrong_contact(
    client: AsyncClient,
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    wrong_phone = PhoneData(
        phone=contact_data.wrong_phone,
    )

    wrong_response = await client.get(
        f"/book/{wrong_phone.phone}",
    )

    data = wrong_response.json()
    assert wrong_response.status_code == 404
    assert "The address cannot be found" in data["detail"]


@pytest.mark.asyncio
async def test_update_contact_data(
    client: AsyncClient,
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    update_data = UpdateBookData(
        phone=contact_data.phone,
        address=contact_data.extra_address,
    )

    response = await client.put(
        "/book/",
        json=update_data.model_dump(),
    )

    data = response.json()
    assert response.status_code == 200
    assert data["phone"] == contact_data.phone_normalized
    assert data["address"] == contact_data.extra_address


@pytest.mark.asyncio
async def test_update_wrong_data(
    client: AsyncClient,
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    wrong_data = UpdateBookData(
        phone=contact_data.wrong_phone,
        address=contact_data.extra_address,
    )

    wrong_response = await client.put(
        "/book/",
        json=wrong_data.model_dump(),
    )

    data = wrong_response.json()
    assert wrong_response.status_code == 404
    assert data["detail"] == "ServiceError: Phone doesn't exists"


@pytest.mark.asyncio
async def test_delete_contact_data(
    client: AsyncClient,
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    test_phone = PhoneData(
        phone=contact_data.phone,
    )

    response = await client.delete(
        f"/book/{test_phone.phone}",
    )

    data = response.json()
    assert response.status_code == 200
    assert data["phone"] == contact_data.phone_normalized
    assert contact_data.phone_normalized in data["delete_message"]


@pytest.mark.asyncio
async def test_delete_wrong_data(
    client: AsyncClient,
    fake_redis: FakeRedis,
    contact_data: ContactData,
) -> None:
    wrong_phone = PhoneData(
        phone=contact_data.wrong_phone,
    )

    wrong_response = await client.delete(
        f"/book/{wrong_phone.phone}",
    )

    data = wrong_response.json()
    assert wrong_response.status_code == 404
    assert data["detail"] == "ServiceError: Phone doesn't exists"

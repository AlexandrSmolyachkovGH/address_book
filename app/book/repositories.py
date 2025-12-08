from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.custom_exceptions.custom_exceptions import (
    RepoError,
)


class BookRepository:
    async def check_conflict_number(
        self,
        phone: str,
        redis_db: Redis,
    ) -> bool:
        try:
            address = await redis_db.get(phone)
        except RedisError as e:
            raise RepoError("Redis error.") from e
        return address is not None

    async def get_address_by_phone(
        self,
        phone: str,
        redis_db: Redis,
    ) -> str | None:
        try:
            address = await redis_db.get(phone)
        except RedisError as e:
            raise RepoError("Redis error.") from e
        return address

    async def create_record(
        self,
        phone: str,
        address: str,
        redis_db: Redis,
    ) -> dict:
        try:
            create_status = await redis_db.set(phone, address)
            if not create_status:
                raise RepoError("Failed to write to Redis DB.")

        except RedisError as e:
            raise RepoError("Redis error.") from e

        return {
            "phone": phone,
            "address": address,
        }

    async def delete_record(
        self,
        phone: str,
        redis_db: Redis,
    ) -> int:
        try:
            delete_res = await redis_db.delete(phone)
        except RedisError as e:
            raise RepoError("Redis error.") from e
        return delete_res

    async def update_contact(
        self,
        phone: str,
        new_address: str,
        redis_db: Redis,
    ) -> dict:
        try:
            await redis_db.set(phone, new_address)
        except RedisError as e:
            raise RepoError("Redis error.") from e
        return {
            "phone": phone,
            "address": new_address,
        }


book_repo = BookRepository()

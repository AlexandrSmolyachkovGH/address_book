from redis.asyncio import Redis

from app.book.repositories import book_repo
from app.custom_exceptions.custom_exceptions import (
    ServiceError,
)
from app.utils.phone_normalization import normalize_phone


class BookService:
    async def get_contact_data(
        self,
        phone: str,
        redis_db: Redis,
    ) -> dict:
        try:
            _phone = normalize_phone(phone)
        except ValueError as e:
            raise ServiceError("Nuber validation failed") from e
        address = await book_repo.get_address_by_phone(
            phone=_phone,
            redis_db=redis_db,
        )
        if address is None:
            raise ServiceError(
                "The address cannot be found for the provided phone.",
            )
        return {
            "phone": _phone,
            "address": address,
        }

    async def create_contact_data(
        self,
        phone: str,
        address: str,
        redis_db: Redis,
    ) -> dict:
        check_conflict = await book_repo.check_conflict_number(
            phone=phone,
            redis_db=redis_db,
        )
        if check_conflict:
            raise ServiceError(
                "Phone already exists",
            )

        contact_dict = await book_repo.create_record(
            phone=phone,
            address=address,
            redis_db=redis_db,
        )
        return contact_dict

    async def delete_contact(
        self,
        phone: str,
        redis_db: Redis,
    ) -> str:
        try:
            _phone = normalize_phone(phone)
        except ValueError as e:
            raise ServiceError("Nuber validation failed") from e

        delete_res = await book_repo.delete_record(
            phone=_phone,
            redis_db=redis_db,
        )
        if not delete_res:
            raise ServiceError(
                "Phone doesn't exists",
            )
        return _phone

    async def update_contact(
        self,
        phone: str,
        new_address: str,
        redis_db: Redis,
    ) -> dict:
        record_check = await book_repo.get_address_by_phone(
            phone=phone,
            redis_db=redis_db,
        )
        if record_check is None:
            raise ServiceError(
                "Phone doesn't exists",
            )
        updated_contact = await book_repo.update_contact(
            phone=phone,
            new_address=new_address,
            redis_db=redis_db,
        )

        return updated_contact


book_service = BookService()

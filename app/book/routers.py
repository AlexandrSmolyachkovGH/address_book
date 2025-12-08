from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    status,
)
from redis.asyncio import Redis

from app.book.schemes import (
    CreateBookData,
    DeleteBookData,
    GetBookData,
    UpdateBookData,
)
from app.book.services import book_service
from app.custom_exceptions.custom_exceptions import ServiceError
from app.db.redis_conn import get_redis

book_router = APIRouter(
    prefix="/book",
    tags=["Book"],
)


@book_router.get(
    path="/{phone}",
    status_code=status.HTTP_200_OK,
    response_model=GetBookData,
    description="Retrieve contact data",
)
async def get_contact_data(
    phone: str,
    redis_db: Annotated[Redis, Depends(get_redis)],
) -> GetBookData:
    """Retrieve a Phone:Address pair from the database"""
    contact_data = await book_service.get_contact_data(
        phone=phone,
        redis_db=redis_db,
    )
    return GetBookData.model_validate(contact_data)


@book_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=GetBookData,
    description="Create new contact record",
)
async def create_contact_data(
    create_data: Annotated[CreateBookData, Body()],
    redis_db: Annotated[Redis, Depends(get_redis)],
) -> GetBookData:
    """Create a Phone:Address pair in the database"""
    try:
        contact_data = await book_service.create_contact_data(
            phone=create_data.phone,
            address=create_data.address,
            redis_db=redis_db,
        )
    except ServiceError as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_409_CONFLICT,
        )
    return GetBookData.model_validate(contact_data)


@book_router.delete(
    path="/{phone}",
    status_code=status.HTTP_200_OK,
    response_model=DeleteBookData,
    description="Delete contact record",
)
async def delete_contact_data(
    phone: str,
    redis_db: Annotated[Redis, Depends(get_redis)],
) -> DeleteBookData:
    """Delete contact data from the database"""
    deleted_phone = await book_service.delete_contact(
        phone=phone,
        redis_db=redis_db,
    )
    delete_message = f"Record with contact {phone} has been deleted"
    return DeleteBookData.model_validate(
        {
            "phone": deleted_phone,
            "delete_message": delete_message,
        }
    )


@book_router.put(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=GetBookData,
    description="Update contact data",
)
async def update_contact_data(
    update_data: Annotated[UpdateBookData, Body()],
    redis_db: Annotated[Redis, Depends(get_redis)],
) -> GetBookData:
    """Set a new address value for the provided phone"""
    updated_data = await book_service.update_contact(
        phone=update_data.phone,
        new_address=update_data.address,
        redis_db=redis_db,
    )
    return GetBookData.model_validate(updated_data)

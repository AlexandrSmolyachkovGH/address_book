from pydantic import (
    BaseModel,
    Field,
    field_validator,
)

from app.utils.phone_normalization import normalize_phone


class PhoneData(BaseModel):
    phone: str = Field(
        description="Phone number in format: +7(XXX)XXX-XX-XX",
        examples=[
            "4951001010",
            "+7(980)666-44-22",
            "8 495 100-50-50",
        ],
    )

    @field_validator('phone')
    def check_phone(cls, value: str) -> str:
        return normalize_phone(value=value)


class AddressData(BaseModel):
    address: str = Field(
        description="Address information of the phone's owner",
        examples=[
            "125 Lenina Street., Apt. 25, Moscow",
            "Москва, ул. Ленина, д. 125, кв. 25",
        ],
    )


class GetBookData(PhoneData, AddressData):
    pass


class CreateBookData(PhoneData, AddressData):
    pass


class DeleteBookData(PhoneData):
    delete_message: str = Field(
        description="Notification about deleting a record",
    )


class UpdateBookData(AddressData, PhoneData):
    pass

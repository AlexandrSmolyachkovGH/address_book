import pytest

from app.book.schemes import ContactData
from app.text_samples.root import RootPageTexts
from app.utils.phone_normalization import normalize_phone


def test_normalize_phone(
    contact_data: ContactData,
) -> None:
    valid_number = normalize_phone(
        value=contact_data.phone,
    )

    assert valid_number == contact_data.phone_normalized


def test_normalize_invalid_phones(
    contact_data: ContactData,
) -> None:
    with pytest.raises(ValueError) as exc_info:
        normalize_phone(value="123")

    with pytest.raises(ValueError) as exc_info_second:
        normalize_phone(value="54951001010")

    assert "failed validation" in str(exc_info.value)
    assert "failed validation" in str(exc_info_second.value)


def test_text_messages() -> None:
    root_title = RootPageTexts.get_root_title()
    root_descr = RootPageTexts.get_root_description()

    assert isinstance(root_title, str)
    assert isinstance(root_descr, str)
    assert root_title == "Address Book Service"
    assert "REST API" in root_descr

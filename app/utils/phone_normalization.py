def normalize_phone(value: str) -> str:
    clean_phone = ''.join(num for num in value if num.isdigit())
    if len(clean_phone) < 10 or len(clean_phone) > 11:
        raise ValueError(
            f"Number {value} failed validation",
        )
    else:
        if len(clean_phone) == 11:
            if clean_phone[0] not in ["7", "8"]:
                raise ValueError(f"Number {value} failed validation")
            clean_phone = clean_phone[1:]

    valid_number = (
        f"+7({clean_phone[:3]})"
        f"{clean_phone[3:6]}-{clean_phone[6:8]}-{clean_phone[8:10]}"
    )

    return valid_number

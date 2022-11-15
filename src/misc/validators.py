import re


def is_valid_name(text: str | None) -> bool:
    if text is None:
        return False
    return True


def is_valid_phone(text: str | None) -> bool:
    if text is None:
        return False

    text = text.replace(" ", "").replace("+", "").replace("-", "")
    if not text.isdigit():
        return False

    return True


def is_valid_email(text: str | None) -> bool:
    if text is None:
        return False

    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if not re.fullmatch(regex, text):
        return False

    return True


def is_valid_address(text: str | None):
    if text is None:
        return False
    return True


def is_valid_helped_with(text: str | None) -> bool:
    if text is None:
        return False

    if len(text) > 50:
        return False

    return True


def is_valid_cleaned(text: str | None) -> bool:
    if text is None:
        return False

    if len(text) > 270:
        return False

    return True


def is_valid_rooms_count(text: str | None) -> bool:
    if text is None:
        return False

    if not text.isdigit():
        return False

    if int(text) <= 0:
        return False
    return True


def is_valid_room_type(text: str | None) -> bool:
    if text is None:
        return False
    return True


def is_valid_room_object(text: str | None) -> bool:
    if text is None:
        return False
    if len(text) > 25:
        return False

    return True

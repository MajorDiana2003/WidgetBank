import pytest

from src.widget import get_date, mask_account_card


# Декоратор для mask_account
@pytest.mark.parametrize(
    "card_or_account, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Счет 64686473678894779589", "Счет **9589"),
    ],
)
def test_mask_account_card(card_or_account: str, expected: str) -> None:
    """Тестирование корректного маскирования карты или счета"""
    assert mask_account_card(card_or_account) == expected


@pytest.mark.parametrize(
    "invalid_input, expected_output",
    [
        ("", "Введен неверный номер карты: "),
        ("Visa 123", "Введена неверная длина номера карты: 123"),
        ("1234567890123456", "Не указан тип карты или счета"),
    ],
)
def test_mask_account_card_invalid(invalid_input: str, expected_output: str) -> None:
    """Тестирование некорректного маскирования карты или счета"""
    with pytest.raises(ValueError) as exc_info:
        mask_account_card(invalid_input)
    assert str(exc_info.value) == expected_output


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2023-10-01", "01.10.2023"),
        ("2024-05-15T12:34:56.789", "15.05.2024"),
        ("2025-12-31", "31.12.2025"),
        ("2026-01-09", "09.01.2026"),
    ],
)
def test_get_date(date_str: str, expected: str) -> None:
    """Тестирование корректного форматирования даты"""
    assert get_date(date_str) == expected

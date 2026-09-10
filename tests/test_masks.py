import pytest

from src.masks import get_mask_account, get_mask_card_number


# Тестирование корректного маскирования номера карты
@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
    ],
)
def test_get_mask_card_number_valid(card_number: str, expected: str) -> None:
    """Тест для проверки маскировки корректного номера карты"""
    assert get_mask_card_number(card_number) == expected


# Тестирование обработки некорректных номеров карт
@pytest.mark.parametrize(
    "invalid_card, expected_error",
    [
        ("1234567890", "Введена неверная длина номера карты: 1234567890"),
        ("", "Введен неверный номер карты: "),
    ],
)
def test_get_mask_card_number_invalid(invalid_card: str, expected_error: str) -> None:
    """Тест для проверки некорректных номеров карт"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(invalid_card)

    assert str(exc_info.value) == expected_error


# Тестирование корректного маскирования номера счета
@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("12345678901234567890", "**7890"),
    ],
)
def test_get_mask_account_valid(account_number: str, expected: str) -> None:
    """Тест для проверки маскировки корректного номера счета"""
    assert get_mask_account(account_number) == expected


# Тестирование маскировки некорректного номера счета
@pytest.mark.parametrize(
    "invalid_account, expected_error",
    [
        ("1234567890", "Введена неверная длинна номера счета: 1234567890"),
        ("", "Введен неверный номер счета: "),
    ],
)
def test_get_mask_account_invalid(invalid_account: str, expected_error: str) -> None:
    """Тест для проверки маскировки некорректного номера счета"""
    assert get_mask_account(invalid_account) == expected_error

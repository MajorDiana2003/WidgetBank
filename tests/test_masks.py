import logging

import pytest
from _pytest.logging import LogCaptureFixture

from src.masks import get_mask_account, get_mask_card_number


# Тестирование корректного маскирования номера карты
@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
    ],
)
def test_get_mask_card_number_valid(card_number: str, expected: str, caplog: LogCaptureFixture) -> None:
    """Тест для проверки маскировки корректного номера карты"""
    with caplog.at_level(logging.INFO):
        assert get_mask_card_number(card_number) == expected
        assert "Номер карты успешно замаскирован." in caplog.text


# Тестирование обработки некорректных номеров карт
@pytest.mark.parametrize(
    "invalid_card, expected_error",
    [
        ("1234567890", "Введена неверная длина номера карты: 1234567890"),
        ("", "Введен неверный номер карты: "),
    ],
)
def test_get_mask_card_number_invalid(invalid_card: str, expected_error: str, caplog: LogCaptureFixture) -> None:
    """Тест для проверки некорректных номеров карт"""
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError) as exc_info:
            get_mask_card_number(invalid_card)

    assert str(exc_info.value) == expected_error
    assert "Ошибка" in caplog.text or "Критическая" in caplog.text


# Тестирование корректного маскирования номера счета
@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("12345678901234567890", "**7890"),
    ],
)
def test_get_mask_account_valid(account_number: str, expected: str, caplog: LogCaptureFixture) -> None:
    """Тест для проверки маскировки корректного номера счета"""
    with caplog.at_level(logging.INFO):
        assert get_mask_account(account_number) == expected
        assert "Номер счета успешно замаскирован." in caplog.text


# Тестирование маскировки некорректного номера счета
@pytest.mark.parametrize(
    "invalid_account, expected_error",
    [
        ("1234567890", "Введена неверная длинна номера счета: 1234567890"),
        ("", "Введен неверный номер счета: "),
    ],
)
def test_get_mask_account_invalid(invalid_account: str, expected_error: str, caplog: LogCaptureFixture) -> None:
    """Тест для проверки маскировки некорректного номера счета"""
    with caplog.at_level(logging.ERROR):
        assert get_mask_account(invalid_account) == expected_error
        assert "Ошибка" in caplog.text or "Критическая" in caplog.text

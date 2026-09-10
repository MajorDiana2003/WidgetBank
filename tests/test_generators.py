from typing import Any, List
import pytest
from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Тесты для filter_by_currency
def test_filter_by_currency_usd(sample_transactions: List[Any]) -> None:
    """Проверка фильтрации по USD"""
    usd_iter = filter_by_currency(sample_transactions, "USD")
    result = list(usd_iter)
    assert len(result) == 3
    assert all(tx["operationAmount"]["currency"]["code"] == "USD" for tx in result)


def test_filter_by_currency_rub(sample_transactions: List[Any]) -> None:
    """Проверка фильтрации по RUB"""
    rub_iter = filter_by_currency(sample_transactions, "RUB")
    result = list(rub_iter)
    assert len(result) == 2
    assert result[0]["operationAmount"]["currency"]["code"] == "RUB"


def test_filter_by_currency_empty(sample_transactions: List[Any]) -> None:
    """Проверка обработки пустого списка и отсутствия нужной валюты"""
    assert list(filter_by_currency([], "USD")) == []
    assert list(filter_by_currency(sample_transactions, "EUR")) == []


# Тесты для transaction_descriptions
def test_transaction_descriptions(sample_transactions: List[Any]) -> None:
    """Проверка возврата корректных описаний"""
    desc_iter = transaction_descriptions(sample_transactions)
    result = list(desc_iter)
    assert result == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]


def test_transaction_descriptions_empty() -> None:
    """Проверка работы с пустым списком транзакций"""
    assert list(transaction_descriptions([])) == []


# Тесты для card_number_generator
@pytest.mark.parametrize(
    "start, end, expected",
    [
        # Обычный диапазон
        (1, 2, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
        # Граничное значение
        (5, 5, ["0000 0000 0000 0005"]),
        # Проверка максимального числа знаков
        (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
    ],
)
def test_card_number_generator(start: int, end: int, expected: List[str]) -> None:
    """ " Параметризованный тест для проверки диапазонов и форматирования"""
    assert list(card_number_generator(start, end)) == expected

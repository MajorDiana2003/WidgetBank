from typing import Any, Dict, Iterable, Iterator


def filter_by_currency(transactions: Iterable[Dict[str, Any]], currency: str = "USD") -> Iterator[Dict[str, Any]]:
    """
    Генератор, который возвращает итератор с транзакциями,
    где валюта соответствует заданной.
    """
    for transaction in transactions:
        if "operationAmount" in transaction:
            if isinstance(transaction, dict) and "operationAmount" in transaction:
                amount_data = transaction["operationAmount"]
                if isinstance(amount_data, dict) and "currency" in amount_data:
                    currency_data = amount_data["currency"]
                    if isinstance(currency_data, dict) and currency_data.get("code") == currency:
                        yield transaction


def transaction_descriptions(transactions: Iterable[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди
    """
    for transaction in transactions:
        description = transaction.get("description", "")
        yield str(description)


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор, который выдает 16-значные номера банковских карт в заданном диапазоне.
    """
    for number in range(start, end + 1):
        card_str = f"{number:016d}"
        formated_card = f"{card_str[0:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
        yield formated_card

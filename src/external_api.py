import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """Принимает словарь с транзакцией и возвращает сумму в рублях (float)."""

    operation_amount = transaction.get("operationAmount") or transaction.get("operation_amount") or {}

    if not operation_amount and "amount" in transaction:
        amount_str = transaction.get("amount")
        currency_info = transaction.get("currency") or {}
    else:
        amount_str = operation_amount.get("amount")
        currency_info = operation_amount.get("currency") or {}

    # Получаем код валюты
    if isinstance(currency_info, dict):
        currency_code = currency_info.get("code")
    else:
        currency_code = str(currency_info)

    if not amount_str or not currency_code:
        return 0.0

    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        return 0.0

    currency_code = currency_code.upper()

    # Если валюта изначально в рублях
    if currency_code in ["RUB", "RUR"]:
        return amount

    # Если валюта требует конвертации
    if currency_code in ["USD", "EUR"]:
        current_api_key = os.getenv("API_KEY") or API_KEY

        if not current_api_key:
            raise ValueError("API_KEY отсутствует в переменных окружения.")

        url = f"https://apilayer.com{currency_code}&symbols=RUB"
        headers = {"apikey": current_api_key}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            rate = float(data["rates"]["RUB"])
            return round(amount * rate, 2)
        except (requests.RequestException, KeyError, ValueError, Exception):
            return 0.0

    return 0.0

from typing import Any, Dict, List
from unittest.mock import Mock, patch

from src.external_api import convert_to_rub


def test_convert_to_rub_rub_direct() -> None:
    """Тест для транзакции в RUB"""
    rub_transaction = {"operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}}}
    assert convert_to_rub(rub_transaction) == 43318.34


@patch("src.external_api.requests.get")
@patch("src.external_api.API_KEY", "mock_key")
def test_convert_to_rub_fixture_usd(mock_get: Mock, sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест успешной конвертации USD с использованием mock ответа API."""
    usd_transaction = sample_transactions[0]

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 80.0}}
    mock_get.return_value = mock_response

    assert convert_to_rub(usd_transaction) == 785925.6


@patch("src.external_api.requests.get")
@patch("src.external_api.API_KEY", "mock_key")
def test_convert_to_rub_api_error(mock_get: Mock, sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест обработки ошибки сети API."""
    usd_transaction = sample_transactions[0]

    mock_get.side_effect = Exception("API Unavailable")
    assert convert_to_rub(usd_transaction) == 0.0

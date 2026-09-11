import json
from unittest.mock import mock_open, patch

from src.utils import tuple_or_list_transactions


def test_tuple_or_list_transactions_success() -> None:
    mock_data = [{"id": 1, "state": "EXECUTED"}]
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        with patch("pathlib.Path.exists", return_value=True):
            assert tuple_or_list_transactions("dummy.json") == mock_data


def test_tuple_or_list_transactions_not_found() -> None:
    with patch("pathlib.Path.exists", return_value=False):
        assert tuple_or_list_transactions("missing.json") == []


def test_tuple_or_list_transactions_invalid_json() -> None:
    with patch("builtins.open", mock_open(read_data="broken")):
        with patch("pathlib.Path.exists", return_value=True):
            assert tuple_or_list_transactions("bad.json") == []

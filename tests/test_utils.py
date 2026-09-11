import json
import logging
from unittest.mock import mock_open, patch

from _pytest.logging import LogCaptureFixture

from src.utils import tuple_or_list_transactions


def test_tuple_or_list_transactions_success(caplog: LogCaptureFixture) -> None:
    mock_data = [{"id": 1, "state": "EXECUTED"}]
    with caplog.at_level(logging.INFO):
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            with patch("pathlib.Path.exists", return_value=True):
                assert tuple_or_list_transactions("dummy.json") == mock_data
                assert "успешно прочитан" in caplog.text


def test_tuple_or_list_transactions_not_found(caplog: LogCaptureFixture) -> None:
    with caplog.at_level(logging.ERROR):
        with patch("pathlib.Path.exists", return_value=False):
            assert tuple_or_list_transactions("missing.json") == []
            assert "Файл не найден по указанному пути" in caplog.text


def test_tuple_or_list_transactions_invalid_json(caplog: LogCaptureFixture) -> None:
    with caplog.at_level(logging.ERROR):
        with patch("builtins.open", mock_open(read_data="broken")):
            with patch("pathlib.Path.exists", return_value=True):
                assert tuple_or_list_transactions("bad.json") == []
                assert "Ошибка при обработке JSON-файла" in caplog.text

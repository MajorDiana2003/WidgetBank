from unittest.mock import MagicMock, patch

from src.file_readers import read_csv_transactions, read_excel_transactions


@patch("src.file_readers.Path.exists")
@patch("pandas.read_csv")
def test_read_csv_transactions_success(mock_read_csv: MagicMock, mock_exists: MagicMock) -> None:
    """Тест успешного чтения CSV-файла."""
    mock_exists.return_value = True

    mock_df = MagicMock()
    mock_df.fillna.return_value = mock_df
    mock_df.to_dict.return_value = [{"id": 123, "state": "EXECUTED"}]
    mock_read_csv.return_value = mock_df

    result = read_csv_transactions("fake_path.csv")
    assert result == [{"id": 123, "state": "EXECUTED"}]


@patch("src.file_readers.Path.exists")
def test_read_csv_transactions_not_found(mock_exists: MagicMock) -> None:
    """Тест поведения, если CSV-файл отсутствует"""
    mock_exists.return_value = False
    result = read_csv_transactions("missing.csv")
    assert result == []


@patch("src.file_readers.Path.exists")
@patch("pandas.read_excel")
def test_read_excel_transactions_success(mock_read_excel: MagicMock, mock_exists: MagicMock) -> None:
    """Тест успешного чтения Excel-файла"""
    mock_exists.return_value = True

    mock_df = MagicMock()
    mock_df.fillna.return_value = mock_df
    mock_df.to_dict.return_value = [{"id": 456, "state": "PENDING"}]
    mock_read_excel.return_value = mock_df

    result = read_excel_transactions("fake_path.xlsx")
    assert result == [{"id": 456, "state": "PENDING"}]


@patch("src.file_readers.Path.exists")
def test_read_excel_transactions_not_found(mock_exists: MagicMock) -> None:
    """Тест поведения, если Excel-файл отсутствует"""
    mock_exists.return_value = False
    result = read_excel_transactions("missing.xlsx")
    assert result == []


import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
    ],
)
def test_filter_by_state_valid(sample_data, state, expected_ids):
    """Тестирование фильтрации списка по разным валидным статусам state"""
    result = filter_by_state(sample_data, state)
    result_ids = [item["id"] for item in result]
    assert result_ids == expected_ids


def test_filter_by_state_default(sample_data):
    """Проверка работы filter_by_state со значением по умолчанию"""
    result = filter_by_state(sample_data)
    result_ids = [item["id"] for item in result]
    assert result_ids == [1, 3]


@pytest.mark.parametrize(
    "non_existent_state",
    [
        "FAILED",
        "UNKNOWN",
        "",
    ],
)
def test_filter_by_state_empty_result(sample_data, non_existent_state):
    """Проверка работы при отсутствии словарей с указанным статусом"""
    result = filter_by_state(sample_data, non_existent_state)
    assert result == []


def test_sort_by_date_default_descending(sample_data):
    """Тестирование сортировки по дате по убыванию"""
    result = sort_by_date(sample_data)
    result_ids = [item["id"] for item in result]
    assert result_ids == [4, 2, 1, 3]


def test_sort_by_date_ascending(sample_data):
    """Тестирование сортировки по дате по возрастанию"""
    result = sort_by_date(sample_data, reverse_order=False)
    result_ids = [item["id"] for item in result]
    assert result_ids == [3, 1, 2, 4]


def test_sort_by_date_empty_list():
    """Проверка сортировки пустого списка"""
    assert sort_by_date([]) == []

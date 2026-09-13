from typing import Any, List

import pytest

from src.processing import filter_by_state, process_bank_operations, process_bank_search, sort_by_date


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
    ],
)
def test_filter_by_state_valid(sample_data: List[Any], state: str, expected_ids: List[int]) -> None:
    """Тестирование фильтрации списка по разным валидным статусам state"""
    result = filter_by_state(sample_data, state)
    result_ids = [item["id"] for item in result]
    assert result_ids == expected_ids


def test_filter_by_state_default(sample_data: List[Any]) -> None:
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
def test_filter_by_state_empty_result(sample_data: List[Any], non_existent_state: str) -> None:
    """Проверка работы при отсутствии словарей с указанным статусом"""
    assert filter_by_state(sample_data, non_existent_state) == []


def test_sort_by_date_default_descending(sample_data: List[Any]) -> None:
    """Тестирование сортировки по дате по убыванию"""
    result = sort_by_date(sample_data)
    result_ids = [item["id"] for item in result]
    assert result_ids == [4, 2, 1, 3]


def test_sort_by_date_ascending(sample_data: List[Any]) -> None:
    """Тестирование сортировки по дате по возрастанию"""
    result = sort_by_date(sample_data, reverse_order=False)
    result_ids = [item["id"] for item in result]
    assert result_ids == [3, 1, 2, 4]


def test_sort_by_date_empty(sample_data: List[Any]) -> None:
    """Проверка сортировки пустого списка"""
    assert sort_by_date([]) == []


def test_process_bank_search_success(sample_data: list[dict[str, Any]]) -> None:
    """Тест успешного поиска операций по слову"""
    result = process_bank_search(sample_data, "Перевод")
    assert isinstance(result, list)


def test_process_bank_search_empty() -> None:
    """Тест поиска с пустым списком"""
    assert process_bank_search(data=[], search="Перевод") == []


def test_process_bank_operations_success(sample_data: list[dict[str, Any]]) -> None:
    """Тест успешного подсчета операций по категориям"""
    categories = ["Перевод организации", "Покупка"]
    result = process_bank_operations(sample_data, categories)
    assert isinstance(result, dict)
    assert "Перевод организации" in result


def test_process_bank_operations_empty(sample_data: list[dict[str, Any]]) -> None:
    """Тест подсчета с пустым списком"""
    assert process_bank_operations(data=[], categories=["Покупка"]) == {"Покупка": 0}

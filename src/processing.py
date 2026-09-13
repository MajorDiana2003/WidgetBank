import logging
import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует словарь по значению ключа state."""
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: List[Dict[str, Any]], reverse_order: bool = True) -> List[Dict[str, Any]]:
    """Сортирует список словарей по дате в указанном порядке(убывание)"""
    return sorted(data, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%dT%H:%M:%S.%f"), reverse=reverse_order)


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Фильтрует список транзакций по заданной строке в описании.
    Использует регулярные выражения для поиска без учета регистра.
    """
    logger.info(f"Начало поиска по описанию транзакций. Строка поиска: '{search}'")
    filtered_data: List[Dict[str, Any]] = []

    try:
        pattern = re.compile(re.escape(search), re.IGNORECASE)

        for operation in data:
            description = operation.get("description")
            if isinstance(description, str) and pattern.search(description):
                filtered_data.append(operation)

        logger.info(f"Поиск успешно завершен. Найдено транзакций: {len(filtered_data)}")
    except Exception as e:
        logger.error(f"Ошибка при выполнении регулярного поиска: {e}")
        filtered_data = []

    return filtered_data


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество банковских операций определенного типа (категорий).
    Возвращает словарь, где ключи - категории, а значения - их количество
    """
    logger.info(f"Начало подсчета транзакций по категориям. Всего категорий для анализа: {len(categories)}")
    result: dict[str, int] = {}

    try:
        all_descriptions = [
            operation.get("description") for operation in data if isinstance(operation.get("description"), str)
        ]

        counts = Counter(all_descriptions)

        for category in categories:
            result[category] = counts[category]

        logger.info("Подсчет по категориям успешно завершен.")
    except Exception as e:
        logger.error(f"Ошибка при подсчете операций по категориям: {e}")
        result = {category: 0 for category in categories}

    return result

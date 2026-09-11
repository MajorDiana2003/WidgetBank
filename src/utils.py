import json
from pathlib import Path
from typing import Any, Dict, List


def tuple_or_list_transactions(file_path: str | Path) -> List[Dict[str, Any]]:
    """Читает JSON-файл с транзакциями и возвращает список словарей"""
    path = Path(file_path)
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, TypeError, OSError):
        return []

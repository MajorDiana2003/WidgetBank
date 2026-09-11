import json
import logging
from pathlib import Path
from typing import Any, Dict, List

# Определение пути к корневой папке logs проекта
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Настройка объекта логера для модуля utils
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Настройка обработчика и формата записи логов
file_handler = logging.FileHandler(LOGS_DIR / "utils.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def tuple_or_list_transactions(file_path: str | Path) -> List[Dict[str, Any]]:
    """Читает JSON-файл с транзакциями и возвращает список словарей"""
    path = Path(file_path)
    logger.debug(f"Попытка чтения файла транзакций по пути: {path}")

    if not path.exists():
        logger.error(f"Файл не найден по указанному пути: {path}")
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, list):
                logger.info(f"Файл {path} успешно прочитан. Возвращен список транзакций.")
                return data

            logger.error(f"Некорректная структура данных в файле {path}: ожидался список, получен {type(data)}")
            return []
    except (json.JSONDecodeError, TypeError, OSError) as e:
        logger.error(f"Ошибка при обработке JSON-файла {path}: {e}")
        return []

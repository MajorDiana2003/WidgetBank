import logging
from pathlib import Path
from typing import Any, Dict, List, cast

import pandas as pd

# Локальный логгер для модуля
logger = logging.getLogger(__name__)


def read_csv_transactions(file_path: str | Path) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла"""
    path = Path(file_path)
    logger.debug(f"Попытка чтения CSV-файла транзакций по пути: {path}")

    if not path.exists():
        logger.error(f"Файл не найден по указанному пути: {path}")
        return []

    try:
        df = pd.read_csv(path, sep=";", encoding="utf-8")
        df = df.fillna("")
        logger.info(f"Файл {path} успешно прочитан.")
        return cast(List[Dict[str, Any]], list(df.to_dict(orient="records")))
    except Exception as e:
        logger.error(f"Ошибка при обработке CSV-файла {path}: {e}")
        return []


def read_excel_transactions(file_path: str | Path) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла"""
    path = Path(file_path)
    logger.debug(f"Попытка чтения EXCEL-файла транзакций по пути: {path}")

    if not path.exists():
        logger.error(f"Файл не найден по указанному пути: {path}")
        return []

    try:
        df = pd.read_excel(path)
        df = df.fillna("")
        logger.info(f"Файл {path} успешно прочитан.")
        return cast(List[Dict[str, Any]], list(df.to_dict(orient="records")))
    except Exception as e:
        logger.error(f"Ошибка при обработке Excel-файла {path}: {e}")
        return []

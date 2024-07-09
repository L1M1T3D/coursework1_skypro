from datetime import datetime, timedelta
from typing import Any

import pandas as pd

from src.utils import configure_logger

log = configure_logger()


def load_transactions_from_excel(path: str) -> pd.DataFrame:
    """Функция загружает транзакции из полученного Excel файла."""
    log.info(f"Загрузка данных из файла {path}")
    try:
        return pd.read_excel(path)
    except FileNotFoundError:
        log.error(f"Файл {path} не найден!")
        return pd.DataFrame()


def filter_transactions_by_category_and_date(transactions: pd.DataFrame, category: str, start_date: str) -> Any:
    """Функция возвращает фильтрованные транзакции по категориям и датам."""
    end_date = datetime.strptime(start_date, "%d.%m.%Y") + timedelta(days=90)
    filtered = transactions[
        (transactions["category"] == category)
        & (transactions["data_payment"] >= start_date)
        & (transactions["data_payment"] < end_date.strftime("d.%m.%Y"))
    ]
    return filtered.to_dict("records")

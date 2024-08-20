from datetime import datetime, timedelta
from typing import Any

import pandas as pd
import json

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
        (transactions["Категория"] == category)
        & (transactions["Дата платежа"] >= start_date)
        & (transactions["Дата платежа"] < end_date.strftime("d.%m.%Y"))
    ]
    return filtered.to_dict("records")


def main_reports() -> None:
    print("Добро пожаловать в модуль отчетов!")

    print("1) Сначала загрузим транзакции из Excel:")
    path = "../data/operations.xls"
    transactions_df = load_transactions_from_excel(path)
    print(transactions_df)

    print("2) Теперь профильтруем транзакции по категории и дате:")
    category = input("Введите категорию для фильтрации: ")
    start_date = input("Введите начальную дату в формате 'DD.MM.YYYY': ")
    transactions_df = load_transactions_from_excel(path)
    filtered_transactions = filter_transactions_by_category_and_date(transactions_df, category, start_date)
    print("-- Отфильтрованные транзакции:")
    print(json.dumps(filtered_transactions, ensure_ascii=False, indent=4))

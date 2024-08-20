import json
import logging
import re
from utils import load_transactions_from_excel

logging.basicConfig(level=logging.INFO)


def find_personal_transfers(transactions: list) -> str:
    """Функция находит и возвращает переводы физическим лицам в формате JSON."""
    pattern = re.compile(r"[А-ЯЁ][а-яё]+ [А-ЯЁ]\.")
    personal_transfers = [
        txn for txn in transactions if txn["Категория"] == "Переводы" and pattern.search(txn["Описание"])
    ]
    return json.dumps(personal_transfers, ensure_ascii=False, indent=4)


def main_services() -> None:
    print("Добро пожаловать в модуль сервисов!")
    print("\nСейчас будет продемонстрирована функция поиска переводов физ. лицам:")

    transactions = load_transactions_from_excel("../data/operations.xls")
    personal_transfers = find_personal_transfers(transactions)
    print("-- Переводы физическим лицам:")
    print(personal_transfers)

import json
import logging
import re

logging.basicConfig(level=logging.INFO)


def find_personal_transfers(transactions: list) -> str:
    """Функция находит и возвращает переводы физическим лицам в формате JSON."""
    pattern = re.compile(r"\b\w+ \w\.\b")
    personal_transfers = [
        txn for txn in transactions if txn["Категория"] == "Переводы" and pattern.search(txn["Описание"])
    ]
    return json.dumps(personal_transfers, ensure_ascii=False, indent=4)
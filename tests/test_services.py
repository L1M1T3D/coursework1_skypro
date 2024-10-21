import json

import pytest

from src.services import find_personal_transfers


@pytest.fixture
def sample_transactions() -> list:
    return [
        {"Категория": "Переводы", "Описание": "Перевод Иванову И.А.", "Сумма платежа": 100},
        {"Категория": "Переводы", "Описание": "Перевод Петрову П.П.", "Сумма платежа": 200},
        {"Категория": "Еда", "Описание": "Обед", "Сумма платежа": 300},
    ]


def test_find_personal_transfers(sample_transactions: list) -> None:
    result = find_personal_transfers(sample_transactions)
    transfers = json.loads(result)
    assert len(transfers) == 2
    assert transfers[0]["Описание"] == "Перевод Иванову И.А."
    assert transfers[1]["Описание"] == "Перевод Петрову П.П."

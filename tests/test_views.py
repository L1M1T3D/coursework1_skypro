from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.utils import load_transactions_from_excel
from src.views import (fetch_currency_rate, fetch_stock_price, generate_greeting, highest_transactions,
                       summarize_card_data, total_expenses)


@pytest.mark.parametrize(
    "user_input, response",
    [
        ("2024-07-09 12:00:00", "Добрый день!"),
        ("2024-07-09 06:00:00", "Доброе утро!"),
        ("2024-07-09 18:00:00", "Добрый вечер!"),
        ("2024-07-09 00:00:00", "Доброй ночи!"),
    ],
)
def test_greeting(user_input: str, response: str) -> None:
    assert generate_greeting(user_input) == response


@patch("requests.get")
def test_fetch_currency_rate(mock_get: Mock) -> None:
    mock_response = Mock()
    mock_response.text = '{"rates": {"RUB": 120}}'
    mock_get.return_value = mock_response
    assert fetch_currency_rate("USD") == 120


@patch("yfinance.Ticker")
def test_fetch_stock_price(mock_ticker: Mock) -> None:
    mock_response = Mock()
    mock_response.history.return_value = pd.DataFrame({"High": [200]})
    mock_ticker.return_value = mock_response
    assert fetch_stock_price("AAPL") == 200


def test_total_expenses() -> None:
    transactions = [{"transaction_amount": -112}, {"transaction_amount": -388}]
    assert total_expenses(transactions) == 500.0


def test_read_excel() -> None:
    with patch("pandas.read_excel", return_value=pd.DataFrame({})):
        assert load_transactions_from_excel("non_file.xls") == []


def test_empty_operations() -> None:
    assert summarize_card_data([]) == []


def test_single_card_transaction() -> None:
    operations = [
        {"card_number": "*1234567890123456", "transaction_amount": -100.0, "bonuses_including_cashback": 5.0}
    ]
    expected_result = [{"last_digits": "3456", "total_spent": 100.0, "cashback": 5.0}]
    assert summarize_card_data(operations) == expected_result


def test_highest_transactions() -> None:
    transactions = [
        {
            "date": "2024-07-05",
            "transaction_amount": -200,
            "category": "Еда",
            "description": "Вкусно-и-точка.",
        },
        {
            "date": "2024-07-01",
            "transaction_amount": -100,
            "category": "Коммунальные услуги",
            "description": "ЖКХ",
        },
    ]
    expected_result = [
        {
            "category": "Коммунальные услуги",
            "date": "2024-07-01",
            "description": "ЖКХ",
            "transaction_amount": -100,
        },
        {
            "category": "Еда",
            "date": "2024-07-05",
            "description": "Вкусно-и-точка.",
            "transaction_amount": -200,
        },
    ]
    assert highest_transactions(transactions) == expected_result

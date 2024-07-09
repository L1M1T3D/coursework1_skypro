from typing import Any
from unittest.mock import patch

import pandas as pd

from src.reports import filter_transactions_by_category_and_date, load_transactions_from_excel


@patch("pandas.read_excel")
def test_load_transactions_success(mock_read_excel: Any) -> None:
    mock_dframe = pd.DataFrame(
        {"category": ["Еда", "ЖКХ"], "data_payment": ["11.04.2020", "05.02.2023"], "amount": [100, 1500]}
    )
    mock_read_excel.return_value = mock_dframe
    result = load_transactions_from_excel("truth_path.xlsx")
    pd.testing.assert_frame_equal(result, mock_dframe)


@patch("pandas.read_excel", side_effect=FileNotFoundError)
def test_load_transactions_faile(mock_read_excel: Any) -> None:
    result = load_transactions_from_excel("none_path.xlsx")
    assert result.empty


def test_filter_transactions() -> None:
    transactions = pd.DataFrame(
        {
            "category": ["Еда", "Еда", "ЖКХ"],
            "data_payment": ["11.04.2020", "12.01.2021", "05.02.2023"],
            "transaction_amount": [100, 500, 300],
        }
    )
    category = "Еда"
    start_date = "11.04.2020"
    exp_res = [
        {"category": "Еда", "data_payment": "11.04.2020", "transaction_amount": 100},
        {"category": "Еда", "data_payment": "12.01.2021", "transaction_amount": 500},
    ]
    result = filter_transactions_by_category_and_date(transactions, category, start_date)
    assert result == exp_res

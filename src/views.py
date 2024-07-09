import json
import os
from datetime import datetime
from typing import Any, Dict, List

import requests
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def generate_greeting(time_str: str | None) -> str:
    """Функция возвращает приветствие, в зависимости от времени суток, полученном на входе функции."""
    date_time = datetime.now() if time_str is None else datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    hour = date_time.hour
    if 5 <= hour < 12:
        return "Доброе утро!"
    elif 12 <= hour < 18:
        return "Добрый день!"
    elif 18 <= hour < 23:
        return "Добрый вечер!"
    return "Доброй ночи!"


def total_expenses(transactions: List[Dict[str, Any]]) -> Any:
    """Функция возвращает общую сумму расходов в полученном списке транзакций."""
    return -sum(t["transaction_amount"] for t in transactions if t["transaction_amount"] < 0)


def summarize_card_data(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Функция обрабатывает данные о картах в полученном списке транзакций."""
    card_summary = {}
    for op in operations:
        if op["card_number"].startswith("*"):
            last_digits = op["card_number"][-4:]
            if last_digits not in card_summary:
                card_summary[last_digits] = {"last_digits": last_digits, "total_spent": 0.0, "cashback": 0.0}
            if op["transaction_amount"] < 0:
                card_summary[last_digits]["total_spent"] += -op["transaction_amount"]
            card_summary[last_digits]["cashback"] += op.get("bonuses_including_cashback", 0.0)
    return list(card_summary.values())


def highest_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Функция возвращает список из пяти самых дорогих транзакций, исходя из полученного списка словарей."""
    return sorted(transactions, key=lambda x: x["transaction_amount"], reverse=True)[:5]


def fetch_currency_rate(currency: str) -> Any:
    """Функция возвращает курс валюты по отношению к рублю, обращаясь к определённому сервису API."""
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    response = requests.get(url, headers={"apikey": API_KEY}, timeout=40)
    return json.loads(response.text)["rates"]["RUB"]


def fetch_stock_price(ticker: str) -> Any:
    """Функция возвращает текущую цену акции с помощью библиотеки Yahoo Finance."""
    stock = yf.Ticker(ticker)
    return stock.history(period="1d")["High"].iloc[0]

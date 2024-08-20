import json
import os
from datetime import datetime
from typing import Any, Dict, List

import requests
import yfinance as yf
from dotenv import load_dotenv

from src.utils import load_transactions_from_excel

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
    return -sum(t["Сумма операции"] for t in transactions if t["Сумма операции"] < 0)


def summarize_card_data(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Функция обрабатывает данные о картах в полученном списке транзакций."""
    card_summary = {}
    for op in operations:
        if str(op["Номер карты"]).startswith("*"):
            last_digits = op["Номер карты"][-4:]
            if last_digits not in card_summary:
                card_summary[last_digits] = {"last_digits": last_digits, "total_spent": 0.0, "cashback": 0.0}
            if op["Сумма операции"] < 0:
                card_summary[last_digits]["total_spent"] += -op["Сумма операции"]
            card_summary[last_digits]["cashback"] += op.get("Бонусы (включая кэшбэк)", 0.0)
    return list(card_summary.values())


def highest_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Функция возвращает список из пяти самых дорогих транзакций, исходя из полученного списка словарей."""
    return sorted(transactions, key=lambda x: x["Сумма операции"], reverse=True)[:5]


def fetch_currency_rate(currency: str) -> Any:
    """Функция возвращает курс валюты по отношению к рублю, обращаясь к определённому сервису API."""
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    response = requests.get(url, headers={"apikey": API_KEY}, timeout=40)
    return json.loads(response.text)["rates"]["RUB"]


def fetch_stock_price(ticker: str) -> Any:
    """Функция возвращает текущую цену акции с помощью библиотеки Yahoo Finance."""
    stock = yf.Ticker(ticker)
    return stock.history(period="1d")["High"].iloc[0]


def main_views() -> None:
    """Главная функция модуля views.py."""
    transactions = load_transactions_from_excel("../data/operations.xls")
    print("Добро пожаловать в модуль работы с данными о транзакциях!")
    print("Давайте начнем с приветствия в зависимости от времени суток.")
    greeting = generate_greeting(None)
    print(greeting)

    print("1) Проверяем общую сумму расходов..")
    expenses = total_expenses(transactions)
    print(f"-- Общая сумма расходов: {expenses}")

    print("2) Вычисляем суммарные данные по картам..")
    summary = summarize_card_data(transactions)
    print("-- Суммарные данные по картам:")
    print(json.dumps(summary, ensure_ascii=False, indent=4))

    print("3) Вычисляем пять самых дорогих транзакций..")
    highest = highest_transactions(transactions)
    print("-- Пять самых дорогих транзакций:")
    print(json.dumps(highest, ensure_ascii=False, indent=4))

    print("4) Узнаём курс валюты к рублю")
    currency = input("Введите код валюты (например, 'USD'): ")
    if os.getenv("API_KEY"):
        rate = fetch_currency_rate(currency)
        print(f"Курс {currency} к рублю: {rate}")
    else:
        print("API_KEY не установлен в .env файле.")

    print("5) Проверяем цену акции..")
    ticker = input("Введите тикер акции (например, 'AAPL'): ")
    price = fetch_stock_price(ticker)
    print(f"Текущая цена акции {ticker}: {price}")

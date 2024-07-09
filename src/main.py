import json
import os
from datetime import datetime

from src.reports import filter_transactions_by_category_and_date, load_transactions_from_excel
from src.services import find_personal_transfers
from src.utils import configure_logger
from src.views import (fetch_currency_rate, fetch_stock_price, generate_greeting, highest_transactions,
                       summarize_card_data, total_expenses)

logger = configure_logger()


def main() -> None:
    """Основная функция программы, использующая все функции для проверки всего проекта."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    greeting = generate_greeting(current_time)
    print(
        f"{greeting} Это предложение было отправлено, исходя из вашего текущего времени!\n"
        f"Это мини-программка для проверки работоспособности всего проекта."
    )

    while True:
        print("\nВыберите функцию для проверки:")
        print("1. Приветствие исходя из времени (уже проверено в начале программы)")
        print("2. Общая сумма расходов")
        print("3. Суммарные данные по картам")
        print("4. Пять самых дорогих транзакций")
        print("5. Курс валюты")
        print("6. Цена акции")
        print("7. Загрузить транзакции из Excel")
        print("8. Фильтрация транзакций по категории и дате")
        print("9. Найти переводы физическим лицам")
        print("0. Выйти")

        choice = input("Введите номер выбранной функции: ")

        if choice == "1":
            time_str = input(
                "Введите дату и время в формате 'YYYY-MM-DD HH:MM:SS' или оставьте пустым для ввода текущего времени: "
            )
            greeting = generate_greeting(time_str if time_str else None)
            print(greeting)

        elif choice == "2":
            transactions = input_transactions()
            expenses = total_expenses(transactions)
            print(f"Общая сумма расходов: {expenses}")

        elif choice == "3":
            transactions = input_transactions()
            summary = summarize_card_data(transactions)
            print("Суммарные данные по картам:")
            print(json.dumps(summary, ensure_ascii=False, indent=4))

        elif choice == "4":
            transactions = input_transactions()
            highest = highest_transactions(transactions)
            print("Пять самых дорогих транзакций:")
            print(json.dumps(highest, ensure_ascii=False, indent=4))

        elif choice == "5":
            currency = input("Введите код валюты (например, 'USD'): ")
            if os.getenv("API_KEY"):
                rate = fetch_currency_rate(currency)
                print(f"Курс {currency} к рублю: {rate}")
            else:
                print("API_KEY не установлен в .env файле.")

        elif choice == "6":
            ticker = input("Введите тикер акции (например, 'AAPL'): ")
            price = fetch_stock_price(ticker)
            print(f"Текущая цена акции {ticker}: {price}")

        elif choice == "7":
            path = input("Введите путь к Excel файлу с транзакциями: ")
            transactions_df = load_transactions_from_excel(path)
            print(transactions_df)

        elif choice == "8":
            path = input("Введите путь к Excel файлу с транзакциями: ")
            category = input("Введите категорию для фильтрации: ")
            start_date = input("Введите начальную дату в формате 'DD.MM.YYYY': ")
            transactions_df = load_transactions_from_excel(path)
            filtered_transactions = filter_transactions_by_category_and_date(transactions_df, category, start_date)
            print("Отфильтрованные транзакции:")
            print(json.dumps(filtered_transactions, ensure_ascii=False, indent=4))

        elif choice == "9":
            transactions = input_transactions()
            personal_transfers = find_personal_transfers(transactions)
            print("Переводы физическим лицам:")
            print(personal_transfers)

        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор, попробуйте снова.")


def input_transactions() -> list[dict]:
    transactions = []
    print("Введите данные транзакций (оставьте поле пустым для завершения ввода):")
    while True:
        transaction_amount = input("Введите сумму транзакции: ")
        if not transaction_amount:
            break
        card_number = input("Введите номер карты: ")
        if not card_number:
            break
        bonuses_including_cashback = input("Введите бонусы, включая кэшбэк: ")
        if not bonuses_including_cashback:
            break
        transactions.append(
            {
                "transaction_amount": float(transaction_amount),
                "card_number": card_number,
                "bonuses_including_cashback": float(bonuses_including_cashback),
            }
        )
    return transactions


if __name__ == "__main__":
    main()

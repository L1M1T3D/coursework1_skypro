# Проект: Финансовый Анализатор

Этот проект представляет собой набор утилит для анализа финансовых транзакций и взаимодействия с различными
 API сервисами. Он включает функции для обработки данных о транзакциях, получения информации о валютных курсах и ценах на акции, а также фильтрации данных по категориям и датам. 

## Выполненные задания из списка:
- **Страница «Главная»** (*«Веб-страницы»*)
- **Траты по категории** (*«Отчеты»*)
- **Поиск переводов физическим лицам** (*«Сервисы»*)

## Структура проекта

- `src/`
  - `main.py` - Основная программа для проверки функциональности всех модулей.
  - `services.py` - Содержит функции для обработки переводов физическим лицам.
  - `views.py` - Включает функции для генерации приветствия, подсчёта расходов, обработки данных о картах, получения 
курсов валют и цен на акции.
  - `reports.py` - Содержит функции для загрузки и фильтрации транзакций из Excel файлов.
  - `utils.py` - Вспомогательные функции, такие как настройка логирования и загрузка транзакций из Excel.

## Установка и настройка

1. Клонируйте репозиторий.

2. Создайте виртуальное окружение и установите зависимости.

3. Создайте файл `.env` в корневой директории проекта и добавьте ваш API ключ:
    ```
    API_KEY=ваш_api_ключ
    ```

## Использование

Запустите `main.py`, чтобы проверить функциональность всех модулей:

```
python src/main.py
```

Следуйте инструкциям на экране для выбора функций и ввода данных. Программа предложит вам различные опции, такие как:
подсчёт расходов, получение курсов валют, фильтрация транзакций и другие.


## Примеры данных

Для проверки функций вам понадобятся примеры данных о транзакциях. Вы можете использовать следующий формат для
создания своих тестовых данных:

```json
[
    {"transaction_amount": -100, "description": "Покупка"},
    {"transaction_amount": -200, "description": "Супермаркет"},
    {"transaction_amount": 300, "description": "Продажа"}
]
```
## Разработчик проекта

**Илья Топко** — миллиардер, плейбой, филантроп

import logging
from logging import Logger
from typing import Any

import pandas as pd


def configure_logger() -> Logger:
    """Настройка логгирования."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="log.txt",
        filemode="w"
    )
    return logging.getLogger(__name__)


def load_transactions_from_excel(path: str) -> Any:
    """Загрузка данных о транзакциях из Excel файла."""
    return pd.read_excel(path).to_dict("records")
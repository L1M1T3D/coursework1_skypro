from src.reports import main_reports
from src.services import main_services
from src.utils import configure_logger
from src.views import main_views

logger = configure_logger()


def main() -> None:
    """Главная функция проекта, вызывает все остальные функции."""
    print("Начинаем выполнение программы.")
    main_views()
    main_reports()
    main_services()
    print("Программа завершена.")


if __name__ == "__main__":
    main()

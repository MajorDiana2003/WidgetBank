import logging
from pathlib import Path
from typing import Any

from src.external_api import convert_to_rub
from src.file_readers import read_csv_transactions, read_excel_transactions
from src.processing import filter_by_state, process_bank_operations, process_bank_search, sort_by_date
from src.utils import tuple_or_list_transactions
from src.widget import get_date, mask_account_card

logger = logging.getLogger(__name__)


def main() -> None:
    """Основная функция программы, реализующая интерфейс пользователя"""
    logger.info("Запуск основного интерфейса программы.")

    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # 1. Выбор типа файла
    while True:
        user_choice = input("\nПользователь: ").strip()
        if user_choice in ("1", "2", "3"):
            logger.info(f"Пользователь выбрал формат файла: {user_choice}")
            break
        print("Программа: Некорректный выбор. Пожалуйста, выберите 1, 2 или 3.")

    data_dir = Path(__file__).resolve().parent / "data"
    transactions: list[dict[str, Any]] = []

    try:
        if user_choice == "1":
            print("Программа: Для обработки выбран JSON-файл.")
            file_path = data_dir / "operations.json"
            transactions = tuple_or_list_transactions(str(file_path))
        elif user_choice == "2":
            print("Программа: Для обработки выбран CSV-файл.")
            file_path = data_dir / "transactions.csv"
            transactions = read_csv_transactions(file_path)
        else:
            print("")
            file_path = data_dir / "transactions_excel.xlsx"
            transactions = read_excel_transactions(file_path)
    except Exception as e:
        logger.error(f"Ошибка при чтении файла данных: {e}")
        print(f"Программа: Произошла ошибка при загрузке данных: {e}")
        return

    # 2. Фильтрация по статусу
    print("\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.")
    print("Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING")

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status_input = input("Пользователь: ").strip()
        status_upper = status_input.upper()
        if status_upper in valid_statuses:
            logger.info(f"Выполняется фильтрация по статусу: {status_upper}")
            print(f"Программа: Операции отфильтрованы по статусу {status_upper}")
            transactions = filter_by_state(transactions, state=status_upper)
            break
        else:
            print(f"Программа: Статус операции '{status_input}'")
            print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
            print("Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING")

    if not transactions:
        print("\nПрограмма: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    # 3. Сортировка по дате
    date_sort_prompt = input("\nПрограмма: Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()
    if date_sort_prompt in ("", "yes", "y"):
        order_prompt = input("Программа: Отсортировать по возрастанию или убыванию?\nПользователь: ").strip().lower()
        reverse = True
        if "возраст" in order_prompt:
            reverse = False
        logger.info(f"Выполняется сортировка по дате. Порядок reverse={reverse}")
        transactions = sort_by_date(transactions, reverse_order=reverse)

    # 4. Фильтрация по валюте
    rub_prompt = input("\nПрограмма: Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower()
    if rub_prompt in ("да", "yes", "y"):
        logger.info("Фильтрация транзакций: только RUB")
        filtered_rub = []
        for t in transactions:
            op_amount = t.get("operationAmount")
            if isinstance(op_amount, dict):
                currency_code = op_amount.get("currency", {}).get("code")
            else:
                currency_code = t.get("currency_code") or t.get("currency_name")

            if currency_code and str(currency_code).strip().upper() == "RUB":
                filtered_rub.append(t)
        transactions = filtered_rub

    # 5. Фильтрация по строке в описании
    search_prompt = (
        input("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ")
        .strip()
        .lower()
    )
    if search_prompt in ("да", "yes", "y"):
        search_word = input("Программа: Введите слово для поиска:\nПользователь: ").strip()
        transactions = process_bank_search(transactions, search_word)

    # 6. Итоговый вывод результатов
    print("\nПрограмма: Распечатываю итоговый список транзакций...")
    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print(f"Программа:\nВсего банковских операций в выборке: {len(transactions)}\n")

    for t in transactions:
        raw_date = t.get("date", "")
        formatted_date = get_date(raw_date) if raw_date else "Дата неизвестна"
        description = t.get("description", "Без описания")

        from_acc = t.get("from")
        to_acc = t.get("to", "")

        masked_from = mask_account_card(from_acc) if from_acc else ""
        masked_to = mask_account_card(to_acc) if to_acc else "Счет назначения неизвестен"

        if masked_from:
            transfer_route = f"{masked_from} -> {masked_to}"
        else:
            transfer_route = masked_to

        op_amount = t.get("operationAmount")
        if isinstance(op_amount, dict) and op_amount:
            amount_val = op_amount.get("amount", "0")
            currency_code = op_amount.get("currency", {}).get("code", "RUB")
        else:
            amount_val = t.get("amount") or t.get("sum") or "0"
            currency_code = t.get("currency_code") or t.get("currency_name") or "RUB"

        if isinstance(currency_code, str):
            currency_code = currency_code.strip().upper()
        else:
            currency_code = "RUB"

        t["amount_str"] = str(amount_val)
        t["currency_code"] = currency_code

        if currency_code not in ("RUB", "РУБ", "РУБ.", "RUR"):
            try:
                converted_val = convert_to_rub(t)

                if converted_val == 0.0 or converted_val is None:
                    amount = amount_val
                    currency = currency_code
                else:
                    amount = converted_val
                    currency = "RUB"
            except Exception:
                logger.error(f"Ошибка конвертации валюты {currency_code}:")
                amount = amount_val
                currency = currency_code
        else:
            amount = amount_val
            currency = "RUB"

        print(f"{formatted_date} {description}")
        print(transfer_route)
        print(f"Сумма: {amount} {currency}\n")

    # Вызов аналитической функции
    print("\nПрограмма: Статистика операций по категориям в текущей выборке:")
    categories_to_count = [
        "Перевод организации",
        "Перевод с карты на карту",
        "Перевод со счета на счет",
        "Открытие вклада",
    ]
    stats = process_bank_operations(transactions, categories_to_count)

    for category, count in stats.items():
        print(f"- {category}: {count} шт.")


if __name__ == "__main__":
    main()

import logging
from pathlib import Path

# Определение пути к корневой папке logs проекта
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Настройка объекта логера для модуля masks
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Настройка обработчика и формата записи логов
file_handler = logging.FileHandler(LOGS_DIR / "masks.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    card_number = card_number.replace(" ", "")
    # проверяем хватает цифр в номере карты
    if not card_number:
        logger.error("Критическая ошибка: Передан пустой номер карты")
        raise ValueError("Введен неверный номер карты: ")

    if len(card_number) != 16 or not card_number.isdigit():
        logger.error(f"Ошибка валидации: Введена неверная длина или формат номера карты: {card_number}")
        raise ValueError(f"Введена неверная длина номера карты: {card_number}")

    result = []  # список для хранения замаскированного номера карты
    counter = 0  # счетчик цифр в номере карты,
    # чтобы знать, какую заменить на *

    for number in card_number:
        counter += 1
        if 6 < counter <= len(card_number) - 4:
            result.append("*")
        else:
            result.append(number)

    masked_card = "".join(result)

    masked_card_result = []  # список для хранения по четыре цифры номера карты

    for i in range(0, len(masked_card), 4):
        masked_card_result.append(masked_card[i : i + 4])

    masked_card_result_with_space = " ".join(masked_card_result)

    logger.info("Номер карты успешно замаскирован.")
    return masked_card_result_with_space


def get_mask_account(card_account: str) -> str:
    """Функция маскировки номера банковского счета"""
    card_account = card_account.replace(" ", "")

    if not card_account:
        logger.error("Критическая ошибка: Передан пустой номер счета")
        return f"Введен неверный номер счета: {card_account}"

    if len(card_account) != 20:
        logger.error(f"Ошибка валидации: Введена неверная длина номера счета: {card_account}")
        return f"Введена неверная длинна номера счета: {card_account}"

    else:
        last_part = str(card_account[-4:])
        logger.info("Номер счета успешно замаскирован.")
        return f"**{last_part}"

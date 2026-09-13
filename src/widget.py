from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(num_for_mask: str) -> str:
    """Функция маскирует номер карты или счета"""
    if not num_for_mask:
        raise ValueError("Введен неверный номер карты: ")

    if not any(c.isalpha() for c in num_for_mask):
        raise ValueError("Не указан тип карты или счета")

    num_for_mask_split = num_for_mask.split()
    if "Счет" in num_for_mask_split:
        return f"Счет {get_mask_account(num_for_mask_split[1])}"
    else:
        card_num = []
        card_name = []
        for i in num_for_mask_split:
            if i.isdigit():
                card_num.append(i)
            if i.isalpha():
                card_name.append(i)
        str_card_num = " ".join(card_num)
        str_card_name = " ".join(card_name)
        return f"{str_card_name} {get_mask_card_number(str_card_num)}"


def get_date(date_inp: str) -> str:
    """Функция, которая принимает на вход строку и возвращает строку с датой."""
    date = datetime.strptime(date_inp[:10], "%Y-%m-%d")
    return f"{date.day:02}.{date.month:02}.{date.year}"

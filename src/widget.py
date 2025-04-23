from src.masks import  get_mask_account
from src.masks import get_mask_card_number
from datetime import datetime
def mask_account_card(num_for_mask: str) -> str:
    """Функция маскирует номер карты или счета"""
    num_for_mask_split = num_for_mask.split()
    if "Счет" in num_for_mask_split:
        return f"Cчет {get_mask_account(num_for_mask_split[1])}"
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
    date = datetime.strptime(date_inp[:10], '%Y-%m-%d')
    return f"{date.day:02}.{date.month:02}.{date.year}"



print(mask_account_card("Maestro 1596837868705199"))
print(mask_account_card("Счет 64686473678894779589"))
print(mask_account_card("MasterCard 7158300734726758"))
print(mask_account_card("Счет 35383033474447895560"))
print(mask_account_card("Visa Classic 6831982476737658"))
print(mask_account_card("Visa Platinum 8990922113665229"))
print(mask_account_card("Visa Gold 5999414228426353"))
print(mask_account_card("Счет 73654108430135874305"))
print(get_date("2024-03-11T02:26:18.671407"))

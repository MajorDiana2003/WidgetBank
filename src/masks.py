def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    card_number = card_number.replace(" ", "")
    # проверяем хватает цифр в номере карты
    if len(card_number) != 16:
        return "Введен неверный номер карты"

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

    return masked_card_result_with_space


def get_mask_account(card_account: str) -> str:
    """Функция маскировки номера банковского счета"""
    card_account = card_account.replace(" ", "")
    last_part = str(card_account[-4:])
    return f"**{last_part}"


print(get_mask_card_number(card_number="1234566789900009"))
print(get_mask_account(card_account="73654108430135874305"))

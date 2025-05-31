from file_utils import load_json, read
import argparse

def luhn_check(card_number: str) -> bool:
    """
    Проверяет номер карты с помощью алгоритма Луна.
    :param Номер карты для проверки.
    :return: True если номер валиден, иначе False.
    """
    if not card_number or len(card_number) != 16 or not card_number.isdigit():
        return False
    tot = 0
    for i, digit in enumerate(card_number):
        num = int(digit)
        if (len(card_number) - i) % 2 == 0:
            num *= 2
            if num > 9:
                num -= 9
        tot += num
    return tot % 10 == 0

def verify_card(card_number: str | None = None) -> None:
    """
    Проверяет номер карты и выводит результат проверки.
    :param Номер карты для проверки.
    """
    if not card_number:
        card_number = read(load_json("settings.json")["output_card_file"])

    if not card_number:
        print("Номер карты не найден. Сначала выполните поиск.")
        return

    print(f"\nПроверка карты: {card_number}")
    is_valid = luhn_check(card_number)
    print(f"Алгоритм Луна: {'VALID' if is_valid else 'INVALID'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', help='Номер карты для проверки')
    args = parser.parse_args()
    verify_card(args.number)
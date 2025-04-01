from file_utils import read, save, ALPH, TEXT, ENCTEXT, KEY

def caesar(text: str, alph: str, key: int) -> str:
    """
        Шифрует текст с помощью шифра Цезаря.

        :param text: Исходный текст для шифрования.
        :param alph: Алфавит, используемый для шифрования.
        :param key: Числовой сдвиг для шифра.
        :return: Зашифрованная строка.
    """
    try:
        enctext = ""
        for char in text:
            match char:
                case c if c in alph:
                    new_index = (alph.index(c) + key) % len(alph)
                    enctext += alph[new_index]
                case c if c.lower() in alph:
                    new_index = (alph.index(c.lower()) + key) % len(alph)
                    enctext += alph[new_index].upper()
                case _:
                    enctext += char
        return enctext
    except Exception as e:
        return f"Ошибка: {e}"

def decrypt_caesar(text: str, alph: str, key: int) -> str:
    """
        Дешифрует текст, зашифрованный шифром Цезаря.
    """
    return caesar(text, alph, -key)

def main() -> None:
    """
        Главная функция программы.

        Читает исходный текст и ключ из файлов, проверяет корректность ключа,
        выполняет шифрование методом Цезаря и сохраняет результат.

        :return: None
        """
    try:
        text = read(TEXT)
        match str(KEY).isdigit():
            case False:
                print("Ошибка: Ключ должен быть числом.")
                return
            case True:
                key = int(KEY)
                enctext = caesar(text, ALPH, key)
                dectext = decrypt_caesar(enctext, ALPH, key)
                print("Исходный текст:")
                print(text)
                print("\n")
                match bool(enctext):
                    case True:
                        print("Зашифрованный текст:")
                        print(enctext)
                        save(ENCTEXT, enctext)
                        print("\nУспешно сохранено:", ENCTEXT)
                        print("\nРасшифрованный текст:")
                        print(dectext)
                    case False:
                        print("\nОшибка при шифровании.")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()

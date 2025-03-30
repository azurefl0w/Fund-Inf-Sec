from settings import ALPH, TEXT, ENCTEXT, KEY

def read(filename: str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Ошибка: {e}"

def save(filename: str, text: str) -> None:
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
    except Exception as e:
        print(f"Ошибка: {e}")

def caesar(text: str, alph: str, key: int) -> str:
    try:
        enctext = ""
        for char in text:
            if char in alph:
                new_index = (alph.index(char) + key) % len(alph)
                enctext += alph[new_index]
            elif char.lower() in alph:
                new_index = (alph.index(char.lower()) + key) % len(alph)
                enctext += alph[new_index].upper()
            else:
                enctext += char
        return enctext
    except Exception as e:
        return f"Ошибка: {e}"

def main() -> None:
    try:
        text = read(TEXT)
        key = read(KEY)

        if not key.isdigit():
            print("Ошибка: Ключ должен быть числом.")
            return
        key = int(key)  # Преобразование в int
        #print(key)
        enctext = caesar(text, ALPH, key)
        if text:
            print("Исходный текст:")
            print(text)
            print("\n")
        if enctext:
            print("Зашифрованный текст:")
            print(enctext)
            save(ENCTEXT, enctext)
            print("\nУспешно сохранено:", ENCTEXT)
        else:
            print("\nОшибка при шифровании.")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()

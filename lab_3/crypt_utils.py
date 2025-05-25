import json

def read_binary_file(file_path: str) -> bytes:
    """
    Читает бинарный файл.
    :param file_path: Путь к файлу
    :return: Содержимое файла или пустой bytes при ошибке
    """
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except Exception as e:
        print(f"Ошибка чтения бинарного файла {file_path}: {e}")
        raise

def write_binary_file(file_path: str, data: bytes):
    """
    Записывает данные в бинарный файл.
    :param file_path: Путь к файлу
    :param data: Данные для записи
    """
    try:
        with open(file_path, 'wb') as f:
            f.write(data)
    except Exception as e:
        print(f"Ошибка записи в бинарный файл {file_path}: {e}")

def load_json_config(config_path: str) -> dict:
    """
    Загружает конфигурацию из JSON файла.
    :param config_path: Путь к файлу
    :return: Словарь с конфигурацией или пустой dict при ошибке
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка чтения файла {config_path}: {e}")
        return {}


from Crypto.Cipher import CAST
from Crypto.Util.Padding import pad, unpad
import os

def create_symmetric_components(key_size: int) -> bytes:
    """
    Генерирует ключ для алгоритма CAST5 с заданным размером.
    :param key_size: Размер ключа
    :return: Ключ в бинарном формате
    """
    if not (40 <= key_size <= 128) or key_size % 8 != 0:
        raise ValueError("Некорректный размер ключа (должен быть 40-128 бит, кратно 8)")
    return os.urandom(key_size // 8)

def encrypt_with_cast5(key: bytes, plaintext: str) -> bytes:
    """
    Шифрует текст алгоритмом CAST5.
    :param key: Ключ шифрования
    :param plaintext: Текст для шифрования
    :return: Зашифрованные данные (IV + ciphertext)
    """
    iv = os.urandom(8)
    cipher = CAST.new(key, CAST.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), 8))
    return iv + ciphertext

def decrypt_with_cast5(key: bytes, ciphertext: bytes) -> str:
    """
    Расшифровывает данные алгоритмом CAST5.
    :param key: Ключ шифрования
    :param ciphertext: Данные для расшифровки (IV + ciphertext)
    :return: Расшифрованный текст
    """
    try:
        iv = ciphertext[:8]
        actual_ciphertext = ciphertext[8:]
        cipher = CAST.new(key, CAST.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(actual_ciphertext), 8)
        return decrypted.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Ошибка дешифрования: {str(e)}")
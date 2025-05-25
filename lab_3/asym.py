from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def generate_rsa_keys():
    """
    Создает пару RSA ключей (2048 бит).
    :return: Приватный и публичный ключи
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key, private_key.public_key()

def save_key_to_pem(key, key_path: str, is_private: bool) -> None:
    """
    Сохраняет ключ в PEM формате.
    :param key: Ключ для сохранения
    :param key_path: Путь для сохранения
    :param is_private: Флаг типа ключа
    """
    try:
        with open(key_path, 'wb') as f:
            if is_private:
                f.write(key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            else:
                f.write(key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
    except Exception as e:
        print(f"Ошибка сохранения ключа: {e}")
        raise

def load_key_from_pem(key_path: str, is_private: bool):
    """
    Загружает ключ из PEM файла.
    :param key_path: Путь к файлу
    :param is_private: Флаг типа ключа
    :return: Загруженный ключ
    """
    try:
        with open(key_path, 'rb') as f:
            data = f.read()
            if is_private:
                return serialization.load_pem_private_key(data, password=None)
            return serialization.load_pem_public_key(data)
    except Exception as e:
        print(f"Ошибка загрузки ключа: {e}")
        raise

def rsa_encrypt(public_key, data: bytes) -> bytes:
    """
    Шифрует данные публичным ключом RSA.
    :param public_key: Публичный ключ
    :param data: Данные для шифрования
    :return: Зашифрованные данные
    """
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def rsa_decrypt(private_key, encrypted_data: bytes) -> bytes:
    """
    Расшифровывает данные приватным ключом RSA.
    :param private_key: Приватный ключ
    :param encrypted_data: Зашифрованные данные
    :return: Расшифрованные данные
    """
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
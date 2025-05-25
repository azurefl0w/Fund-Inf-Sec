import argparse
import sys
from sym import *
from asym import *
from file_utils import read, save
from crypt_utils import read_binary_file, write_binary_file, load_json_config

def setup_keys(enc_key_path: str, key_size: int,
               public_key_path: str, private_key_path: str):
    """Генерирует и сохраняет криптографические ключи"""
    try:
        cast_key = create_symmetric_components(key_size)
        priv_key, pub_key = generate_rsa_keys()

        save_key_to_pem(pub_key, public_key_path, False)
        save_key_to_pem(priv_key, private_key_path, True)

        encrypted_key = rsa_encrypt(pub_key, cast_key)
        write_binary_file(enc_key_path, encrypted_key)

        print("Ключи успешно созданы и сохранены")
    except Exception as e:
        print(f"Ошибка при генерации ключей: {e}")
        sys.exit(1)

def encrypt_data(input_path: str, priv_key_path: str,
                 enc_key_path: str, output_path: str):
    """Шифрует данные гибридной системой"""
    try:
        text_data = read(input_path)
        priv_key = load_key_from_pem(priv_key_path, True)
        enc_key = read_binary_file(enc_key_path)

        sym_key = rsa_decrypt(priv_key, enc_key)
        encrypted_data = encrypt_with_cast5(sym_key, text_data)

        write_binary_file(output_path, encrypted_data)
        print("Данные успешно зашифрованы")
    except Exception as e:
        print(f"Ошибка при шифровании: {e}")
        sys.exit(1)

def decrypt_data(input_path: str, priv_key_path: str,
                 enc_key_path: str, output_path: str):
    """Расшифровывает данные гибридной системой"""
    try:
        priv_key = load_key_from_pem(priv_key_path, True)
        enc_key = read_binary_file(enc_key_path)
        enc_data = read_binary_file(input_path)

        sym_key = rsa_decrypt(priv_key, enc_key)
        result = decrypt_with_cast5(sym_key, enc_data)

        save(output_path, result)

        print("Данные успешно расшифрованы")
    except Exception as e:
        print(f"Ошибка при дешифровании: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generate', action='store_true',
                       help='Режим генерации ключей')
    group.add_argument('-enc', '--encrypt', action='store_true',
                       help='Режим шифрования')
    group.add_argument('-dec', '--decrypt', action='store_true',
                       help='Режим дешифрования')

    args = parser.parse_args()

    try:
        config = load_json_config('settings.json')['settings']

        if args.generate:
            setup_keys(
                config['sym_key'],
                int(config['len_key']),
                config['publ_key'],
                config['priv_key']
            )
        elif args.encrypt:
            encrypt_data(
                config['orig_file'],
                config['priv_key'],
                config['sym_key'],
                config['enc_file']
            )
        elif args.decrypt:
            decrypt_data(
                config['enc_file'],
                config['priv_key'],
                config['sym_key'],
                config['dec_file']
            )
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
import hashlib
import multiprocessing as mp
from file_utils import save, load_json
from tqdm import tqdm
import sys
import time

def check_hash(args: tuple[str, str, str]) -> str | None:
    """
    Проверяет хеш номера карты.
    :param Кортеж (номер карты, целевой хеш, алгоритм хеширования).
    :return: Номер карты если хеш совпадает, иначе None.
    """
    card, target_hash, algorithm = args
    if len(card) != 16 or not card.isdigit():
        return None
    h = hashlib.new(algorithm)
    h.update(card.encode('utf-8'))
    return card if h.hexdigest() == target_hash else None

def generate_tasks(bins: list[str], last_four: str,
                   target_hash: str, algorithm: str) -> list[tuple[str, str, str]]:
    """
    Генерирует задачи для проверки хешей.
    :param bins: Список BIN-ов карт.
    :param last_four: Последние 4 цифры номера карты.
    :param target_hash: Целевой хеш для поиска.
    :param algorithm: Алгоритм хеширования.
    :return: Список задач для проверки.
    """
    tasks = []
    for bin in bins:
        for i in range(10 ** 6):
            tasks.append((f"{bin}{i:06d}{last_four}", target_hash, algorithm))
    return tasks

def find_card(processes: int | None = None) -> tuple[str | None, float]:
    """
    Ищет номер карты по хешу с использованием многопроцессорности.
    :param Количество процессов для использования (по умолчанию - все ядра).
    :return: Кортеж (найденный номер карты или None, время выполнения).
    """
    config = load_json("settings.json")
    try:
        if len(config["last_four"]) != 4:
            raise ValueError("Последние цифры должны быть 4")

        processes = min(processes or mp.cpu_count(), 16)
        print(f"\nПоиск карты: ******{config['last_four']}")
        print(f"Используется {processes} процессов, алгоритм {config['hash_algorithm']}")
        print(f"Проверяем {len(config['vtb_mastercard_credit_bins'])} BIN ВТБ Mastercard Credit")

        start_time = time.time()

        tasks = generate_tasks(
            config['vtb_mastercard_credit_bins'],
            config['last_four'],
            config['hash'],
            config['hash_algorithm']
        )

        with mp.Pool(processes=processes) as pool:
            total_tasks = len(config['vtb_mastercard_credit_bins']) * 10 ** 6

            for result in tqdm(pool.imap_unordered(check_hash, tasks, chunksize=10000),
                               total=total_tasks,
                               desc="Перебор комбинаций"):
                if result:
                    duration = time.time() - start_time
                    save(config["output_card_file"], result)
                    print(f"\nНайден номер карты: {result}")
                    print(f"Время поиска: {duration:.2f} секунд")
                    pool.terminate()
                    return result, duration

        duration = time.time() - start_time
        print("\nКарта не найдена.")
        return None, duration

    except Exception as e:
        print(f"\nОшибка: {e}", file=sys.stderr)
        return None, 0

if __name__ == "__main__":
    find_card()
import math
from scipy.special import erfc, gammaincc
from file_utils import load_json

def frequency_test(sequence: str) -> float:
    """
    Частотный побитовый тест
    Проверяет, является ли количество единиц и нулей в последовательности примерно одинаковым.

    :param sequence: Битовая строка для анализа
    :return: P-значение теста
    """
    if not sequence:
        return 0

    n = len(sequence)
    try:
        s_n = sum(1 if bit == '1' else -1 for bit in sequence) / math.sqrt(n)
        return erfc(abs(s_n) / math.sqrt(2))
    except ZeroDivisionError:
        return 0


def runs_test(sequence: str) -> float:
    """
    Тест на одинаковые подряд идущие биты
    Проверяет случайность чередований битов в последовательности.

    :param sequence: Битовая строка для анализа
    :return: P-значение теста
    """
    if not sequence:
        return 0

    n = len(sequence)
    pi = sequence.count('1') / n

    # Проверка предварительного условия
    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return 0

    v_n = sum(0 if sequence[i] == sequence[i + 1] else 1
              for i in range(n - 1))

    try:
        denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
        return erfc(abs(v_n - 2 * n * pi * (1 - pi)) / denominator)
    except ZeroDivisionError:
        return 0


def longest_run_test(sequence: str, block_size: int = 8) -> float:
    """
    Тест на самую длинную последовательность единиц в блоке
    Анализирует распределение максимальных длин последовательностей единиц.

    :param sequence: Битовая строка для анализа
    :param block_size: Размер блока для анализа (по умолчанию 8)
    :return: P-значение теста
    """
    if not sequence or len(sequence) < block_size:
        return 0

    n = len(sequence)
    num_blocks = n // block_size
    v = [0, 0, 0, 0]  # v0, v1, v2, v3

    for i in range(num_blocks):
        block = sequence[i * block_size: (i + 1) * block_size]
        max_run = current_run = 0

        for bit in block:
            current_run = current_run + 1 if bit == '1' else 0
            max_run = max(max_run, current_run)

        match max_run:
            case x if x <= 1:
                v[0] += 1
            case 2:
                v[1] += 1
            case 3:
                v[2] += 1
            case _:
                v[3] += 1

    settings = load_json("settings.json")
    pi = [float(x) for x in settings["PROBABILITIES"]]
    try:
        chi_square = sum((v[i] - num_blocks * pi[i]) ** 2 / (num_blocks * pi[i])
                         for i in range(4))
        return gammaincc(1.5, chi_square / 2)
    except ZeroDivisionError:
        return 0
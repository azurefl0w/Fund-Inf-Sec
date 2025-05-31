import matplotlib.pyplot as plt
from numb_selection import find_card
import multiprocessing as mp
from tqdm import tqdm
from file_utils import load_json

def plot_time_graph() -> None:
    """
    Строит график зависимости времени от количества процессов.
    Сохраняет график в файл, указанный в settings.json.
    """
    config = load_json("settings.json")
    cores = mp.cpu_count()
    max_p = int(cores)
    process_counts = range(1, max_p + 1)
    times = []

    print(f"Тестирование производительности (1-{max_p} процессов)")

    for n in tqdm(process_counts, desc="Замер времени"):
        _, duration = find_card(n)
        times.append(duration)

    plt.figure(figsize=(10, 5))
    plt.plot(process_counts, times, 'b-o')
    plt.xlabel('Количество процессов')
    plt.ylabel('Время (сек)')
    plt.title('Зависимость времени поиска от числа процессов')
    plt.grid(True)

    min_time = min(times)
    min_index = times.index(min_time)
    plt.scatter([process_counts[min_index]], [min_time], color='red',
                label=f'Оптимум: {process_counts[min_index]} процессов')
    plt.legend()

    plt.savefig(config["graph_output"])
    print(f"\nГрафик сохранен как {config['graph_output']}")


if __name__ == "__main__":
    plot_time_graph()
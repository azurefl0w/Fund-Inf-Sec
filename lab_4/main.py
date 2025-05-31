import argparse
from numb_selection import find_card
from luhn import verify_card
from graph import plot_time_graph

def main() -> None:
    """
    Основная функция, обрабатывающая аргументы командной строки.
    Запускает соответствующие функции в зависимости от команды.
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    find_parser = subparsers.add_parser('find', help='Поиск номера карты по хешу')
    find_parser.add_argument('-p', '--processes', type=int,
                           help='Количество процессов (по умолчанию - все ядра)')
    verify_parser = subparsers.add_parser('verify', help='Проверка карты алгоритмом Луна')
    verify_parser.add_argument('-n', '--number', help='Проверить конкретный номер карты')
    graph_parser = subparsers.add_parser('graph', help='Построение графика производительности')

    args = parser.parse_args()

    match args.command:
        case 'find':
            find_card(args.processes)
        case 'verify':
            verify_card(args.number)
        case 'graph':
            plot_time_graph()
        case _:
            print("Неизвестная команда")

if __name__ == "__main__":
    main()
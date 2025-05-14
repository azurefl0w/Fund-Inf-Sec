#include <iostream>
#include <fstream>
#include <random>
#include <bitset>

int main() {
/**
     * @details
     * 1. Использует генератор случайных чисел (`std::random_device`)
     * 2. Применяет вихрь Мерсенна (`std::mt19937`) для генерации
     * 3. Сохраняет результат в файл
     *
     * @return 0 при успешном выполнении
*/
    const int N = 128; ///< Длина битовой последовательности
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 1); ///< Равномерное распределение

    std::bitset<N> sequence;
    for (int i = 0; i < N; ++i) {
        sequence[i] = dis(gen);
    }

    std::ofstream out("task1/cgen_sequence.txt");
    out << sequence;
    out.close();

    return 0;
}
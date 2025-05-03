#include <iostream>
#include <fstream>
#include <random>
#include <bitset>

int main() {
    const int N = 128;
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 1);

    std::bitset<N> sequence;
    for (int i = 0; i < N; ++i) {
        sequence[i] = dis(gen);
    }

    std::ofstream out("task1/cgen_sequence.txt");
    out << sequence;
    out.close();

    return 0;
}
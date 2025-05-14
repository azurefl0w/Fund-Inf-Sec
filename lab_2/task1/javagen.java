import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;



public class javagen {
    public static void main(String[] args) throws IOException {
    /**
         * Генерирует последовательность случайных битов (0 и 1) и сохраняет её в файл
         *
         * @param args Аргументы командной строки (не используются)
         * @throws IOException Если происходит ошибка при записи в файл
    */
        int N = 128; ///< Длина битовой последовательности
        Random rand = new Random();
        StringBuilder sequence = new StringBuilder();

        for (int i = 0; i < N; i++) {
            sequence.append(rand.nextInt(2));
        }

        FileWriter out = new FileWriter("task1/javagen_sequence.txt");
        out.write(sequence.toString());
        out.close();
    }
}
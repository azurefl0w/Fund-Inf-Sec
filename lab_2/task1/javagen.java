import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class javagen {
    public static void main(String[] args) throws IOException {
        int N = 128;
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
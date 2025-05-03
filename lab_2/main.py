import subprocess
from file_utils import read, save, load_json
from task2.tests import frequency_test, runs_test, longest_run_test

settings = load_json("settings.json")
c_sequence = read(settings["CGEN_SEQ_PATH"])
java_sequence = read(settings["JAVAGEN_SEQ_PATH"])
result_path = settings["RESULTS_PATH"]
numbits = settings["NUMBITS"]

def generate_sequences():
    try:
        # Генерация последовательности на c++
        subprocess.run(["g++", "task1/cgen.cpp", "-o", "task1/cgen"], check=True)
        subprocess.run(["./task1/cgen"], check=True)

        # Генерация последовательности на java
        subprocess.run(["javac", "task1/javagen.java"], check=True)
        subprocess.run(["java", "-cp", "task1", "javagen"], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при генерации последовательностей: {e}")
        raise

def run_tests():
    try:
        results = "Результаты тестирования\n\n"
        results += "C Sequence:\n"
        results += f"Frequency Test: {frequency_test(c_sequence):.10f}\n"
        results += f"Runs Test: {runs_test(c_sequence):.10f}\n"
        results += f"Longest Run Test: {longest_run_test(c_sequence):.10f}\n\n"

        results += "Java Sequence:\n"
        results += f"Frequency Test: {frequency_test(java_sequence):.10f}\n"
        results += f"Runs Test: {runs_test(java_sequence):.10f}\n"
        results += f"Longest Run Test: {longest_run_test(java_sequence):.10f}\n\n"

        results += "Критерий прохождения: P-value ≥ 0.01"

        save(result_path, results)
        print(results)

    except Exception as e:
            print(f"Ошибка при выполнении тестов: {e}")
            raise

if __name__ == "__main__":
    generate_sequences()
    run_tests()
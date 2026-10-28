import threading
import time
import sys


# Calculate the nth Fibonacci number.
# This function assumes n is a non-negative integer.
def fibonacci(n):
    if n <= 1:
        return n

    a, b = 0, 1

    # The loop runs n - 1 times.
    for i in range(2, n + 1):
        a, b = b, a + b

    return b


# Calculate the three Fibonacci numbers using three worker threads.
def with_multithreading():
    results = [0, 0, 0]
    start_times = [0, 0, 0]
    end_times = [0, 0, 0]

    # Each worker uses its own position in the lists.
    def calculate(index, n):
        # Record when this worker begins its calculation.
        start_times[index] = time.perf_counter_ns()

        results[index] = fibonacci(n)

        # Record when this worker finishes its calculation.
        end_times[index] = time.perf_counter_ns()

    # Create exactly three workers, one for each input.
    thread1 = threading.Thread(target=calculate, args=(0, 35))
    thread2 = threading.Thread(target=calculate, args=(1, 38))
    thread3 = threading.Thread(target=calculate, args=(2, 40))

    # Start all workers before waiting for them.
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait until all three workers have finished.
    thread1.join()
    thread2.join()
    thread3.join()

    # Assignment formula:
    # Latest worker finish - Earliest worker start.
    elapsed_time = max(end_times) - min(start_times)

    return results, elapsed_time


# Calculate the same numbers sequentially.
def without_multithreading():
    results = [0, 0, 0]

    start_time = time.perf_counter_ns()

    results[0] = fibonacci(35)
    results[1] = fibonacci(38)
    results[2] = fibonacci(40)

    end_time = time.perf_counter_ns()

    elapsed_time = end_time - start_time

    return results, elapsed_time


def main():
    # Display information about the Python runtime.
    print("Python version:", sys.version.split()[0])
    print("Implementation:", sys.implementation.name)

    if hasattr(sys, "_is_gil_enabled"):
        print("GIL enabled:", sys._is_gil_enabled())
    else:
        print("GIL status: not available through this runtime check")

    # Experiment 1: ten rounds with multithreading.
    print("\n=== Fibonacci Computation With Multithreading ===")

    threaded_total = 0

    for round_number in range(1, 11):
        results, elapsed_time = with_multithreading()

        threaded_total = threaded_total + elapsed_time

        # Printing happens outside the timed calculation interval.
        print(
            f"Round {round_number:2}: "
            f"Fib(35)={results[0]}, "
            f"Fib(38)={results[1]}, "
            f"Fib(40)={results[2]} | "
            f"T = {elapsed_time:,} ns"
        )

    threaded_average = threaded_total / 10

    print(f"\nTotal time for 10 rounds: {threaded_total:,} ns")
    print(f"Average time: {threaded_average:,.1f} ns")

    # Experiment 2: ten rounds without multithreading.
    print("\n=== Fibonacci Computation Without Multithreading ===")

    sequential_total = 0

    for round_number in range(1, 11):
        results, elapsed_time = without_multithreading()

        sequential_total = sequential_total + elapsed_time

        print(
            f"Round {round_number:2}: "
            f"Fib(35)={results[0]}, "
            f"Fib(38)={results[1]}, "
            f"Fib(40)={results[2]} | "
            f"T = {elapsed_time:,} ns"
        )

    sequential_average = sequential_total / 10

    print(f"\nTotal time for 10 rounds: {sequential_total:,} ns")
    print(f"Average time: {sequential_average:,.1f} ns")

    # Compare the measured averages.
    print("\n=== Comparison ===")
    print(f"With multithreading: {threaded_average:,.1f} ns")
    print(f"Without multithreading: {sequential_average:,.1f} ns")

    if threaded_average < sequential_average:
        print("Multithreading was faster in this experiment.")
    elif threaded_average > sequential_average:
        print("Sequential execution was faster in this experiment.")
    else:
        print("Both approaches had the same average time.")

    # Avoid dividing by zero if the timer reports a zero average.
    if sequential_average > 0:
        improvement = (
            (sequential_average - threaded_average)
            / sequential_average
        ) * 100

        print(f"Time reduction from multithreading: {improvement:.2f}%")
        print("A negative percentage means multithreading took longer.")

    print(
        "\nThese calculations are short, so scheduling, "
        "timer overhead and background activity can affect the results."
    )


# Start the experiments when this file is run directly.
if __name__ == "__main__":
    main()
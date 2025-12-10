# QuickSort_Performance.py
"""
Performance benchmark harness for Python sorting algorithms.

Assumes each algorithm is a function:
    def quicksort(a: list[int]) -> None
"""

from __future__ import annotations
from typing import Callable, Dict, List, Tuple
import random
import time
import statistics
import csv

# Import Algorithms

from QuickSort_ChatGPT import quicksort as quicksort_chatgpt
from QuickSort_Claude import quicksort as quicksort_claude
from QuickSort_DeepSeek import quicksort as quicksort_deepseek
from QuickSort_Gemini import quicksort as quicksort_gemini

SortFunc = Callable[[List[int]], None]

ALGORITHMS: Dict[str, SortFunc] = {
    "chatgpt" : quicksort_chatgpt,
    "claude" : quicksort_claude,
    "deepseek" : quicksort_deepseek,
    "gemini" : quicksort_gemini,
}

# Test Case Generators

def gen_random(n: int) -> List[int]:
    return [random.randint(-10**6, 10**6) for _ in range(n)]

def gen_sorted(n: int) -> List[int]:
    arr = gen_random(n)
    arr.sort()
    return arr

def gen_reversed(n: int) -> List[int]:
    arr = gen_random(n)
    arr.sort(reverse=True)
    return arr

def gen_nearly_sorted(n: int) -> List[int]:
    """Start sorted, then do a few random swaps."""
    arr = gen_sorted(n)
    if n <= 1:
        return arr
    num_swaps = max(1, n // 100)
    for _ in range(num_swaps):
        i = random.randrange(n)
        j = random.randrange(n)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def gen_few_values(n: int) -> List[int]:
    """Many duplicates: values from a small range."""
    return [random.randint(0, 9) for _ in range(n)]

DISTRIBUTIONS: Dict[str, Callable[[int], List[int]]] = {
    "random": gen_random,
    "sorted": gen_sorted,
    "reversed": gen_reversed,
    "nearly_sorted": gen_nearly_sorted,
    "few_values": gen_few_values,
}

SIZES = [50, 100, 200, 500]
RUNS_PER_COMBO = 10  # how many timing runs per (algo, dist, size)

# Benchmark logic

def precompute_inputs() -> Dict[Tuple[str, int, int], List[int]]:
    """
    Precompute base arrays so every algorithm sees identical inputs.

    Key is (dist_name, size, run_index) -> list[int]
    """
    inputs: Dict[Tuple[str, int, int], List[int]] = {}
    for dist_name, generator in DISTRIBUTIONS.items():
        for n in SIZES:
            for run_idx in range(RUNS_PER_COMBO):
                inputs[(dist_name, n, run_idx)] = generator(n)
    return inputs

def time_one_run(sort_func: SortFunc, arr: List[int]) -> float:
    """Time a single call to sort_func on a copy of arr."""
    a = list(arr)  
    t0 = time.perf_counter()
    sort_func(a)
    t1 = time.perf_counter()
    return t1 - t0

def benchmark() -> List[Dict[str, object]]:

    random.seed(1)  # for reproducibility
    base_inputs = precompute_inputs()

    results: List[Dict[str, object]] = []

    for algo_name, sort_func in ALGORITHMS.items():
        print(f"Benchmarking algorithm: {algo_name}")

        for dist_name in DISTRIBUTIONS.keys():
            for n in SIZES:
                durations: List[float] = []

                # multiple runs
                for run_idx in range(RUNS_PER_COMBO):
                    arr = base_inputs[(dist_name, n, run_idx)]
                    dt = time_one_run(sort_func, arr)
                    durations.append(dt)

                durations.sort()
                median = statistics.median(durations)
                mean = statistics.mean(durations)
                min_t = durations[0]
                max_t = durations[-1]

                print(
                    f"{dist_name:13s} | n={n:4d} | "
                    f"median={median:.6f}s | mean={mean:.6f}s | "
                    f"min={min_t:.6f}s | max={max_t:.6f}s"
                )

                results.append(
                    {
                        "algorithm": algo_name,
                        "distribution": dist_name,
                        "n": n,
                        "runs": RUNS_PER_COMBO,
                        "median_sec": median,
                        "mean_sec": mean,
                        "min_sec": min_t,
                        "max_sec": max_t,
                    }
                )

        print()

    print("All benchmarks completed.")
    return results

def write_csv(results: List[Dict[str, object]], filename: str = "python_bench_results.csv") -> None:
    if not results:
        print("No results to write.")
        return

    fieldnames = list(results[0].keys())
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Results written to {filename}")

if __name__ == "__main__":
    res = benchmark()
    write_csv(res)

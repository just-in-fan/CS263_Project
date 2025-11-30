# QuickSort_Correctness.py
"""
Correctness test harness for Python sorting algorithms.

Assumes each algorithm is a function:
    def quicksort(a: list[int]) -> None
"""

from __future__ import annotations
from typing import Callable, Dict, List, Tuple
import random
import traceback

# Import Algorithms

from QuickSort_ChatGPT import quicksort as quicksort_chatgpt
from QuickSort_Claude import quicksort as quicksort_claude
from QuickSort_DeepSeek import quicksort as quicksort_deepseek
from QuickSort_Gemini import quicksort as quicksort_gemini

SortFunc = Callable[[List[int]], None]

ALGORITHMS: Dict[str, SortFunc] = {
    "Chatgpt" : quicksort_chatgpt,
    "Claude" : quicksort_claude,
    "Deepseek" : quicksort_deepseek,
    "Gemini" : quicksort_gemini,
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

EDGE_CASES: List[List[int]] = [
    [],
    [1],
    [1, 1, 1],
    [0, -1, 5, -1],
    [2, 1],
    [2, 2, 1, 1],
    [5, 4, 3, 2, 1],
]

DISTRIBUTIONS: Dict[str, Callable[[int], List[int]]] = {
    "random": gen_random,
    "sorted": gen_sorted,
    "reversed": gen_reversed,
    "nearly_sorted": gen_nearly_sorted,
    "few_values": gen_few_values,
}

SIZES = [0, 1, 2, 5, 10, 100, 1000, 5000]
CASES_PER_COMBO = 20  # number of random arrays per (distribution, size)

# Run Tests

def run_correctness_tests() -> None:

    random.seed(1)  # for reproducibility

    for algo_name, sort_func in ALGORITHMS.items():
        print("=" * 70)
        print(f"Testing algorithm: {algo_name}")
        total_tests = 0
        total_failures = 0
        total_exceptions = 0

        # Edge cases first
        print("  Edge cases:")
        for idx, case in enumerate(EDGE_CASES):
            total_tests += 1
            arr = list(case)
            expected = sorted(case)
            try:
                sort_func(arr)
                if arr != expected:
                    total_failures += 1
                    print(f"    FAIL edge_case[{idx}]: input={case}, got={arr}, expected={expected}")
            except Exception as e:
                total_exceptions += 1
                #print(f"    EXCEPTION edge_case[{idx}]: {e}")
                #traceback.print_exc(limit=1)

        # Randomized distributions
        print("  Randomized distributions:")
        for dist_name, generator in DISTRIBUTIONS.items():
            dist_tests = 0
            dist_failures = 0
            dist_exceptions = 0

            for n in SIZES:
                for _ in range(CASES_PER_COMBO):
                    arr = generator(n)
                    expected = sorted(arr)
                    test_input = list(arr)  # keep original for debugging
                    total_tests += 1
                    dist_tests += 1
                    try:
                        sort_func(arr)
                        if arr != expected:
                            total_failures += 1
                            dist_failures += 1
                            print(
                                f"    FAIL {dist_name}, n={n}: "
                                f"input(sample)={test_input[:10]}, "
                                f"got(sample)={arr[:10]}, expected(sample)={expected[:10]}"
                            )
                    except Exception as e:
                        total_exceptions += 1
                        dist_exceptions += 1
                        #print(f"    EXCEPTION {dist_name}, n={n}: {e}")
                        #traceback.print_exc(limit=1)

            print(
                f"    {dist_name}: tests={dist_tests}, "
                f"failures={dist_failures}, exceptions={dist_exceptions}"
            )

        print("-" * 70)
        print(
            f"Summary for {algo_name}: "
            f"tests={total_tests}, failures={total_failures}, exceptions={total_exceptions}"
        )
        print()

    print("All correctness tests completed.")


if __name__ == "__main__":
    run_correctness_tests()

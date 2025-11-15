import random

TEST_CASES = {
    "empty": [],
    "single_element": [5],
    "already_sorted": [1, 2, 3, 4, 5],
    "reverse_sorted": [5, 4, 3, 2, 1],
    "random_small": [3, 1, 4, 1, 5],
    "random_large": [random.randint(1, 1000) for _ in range(1000)],
    "duplicates_heavy": [1, 3, 2, 1, 3, 2, 1],
    "negative_numbers": [-5, 2, -3, 0, -1, 4],
    "floating_point": [3.14, 1.41, 2.71, 0.0, -1.0],
    "edge_case_large_range": [1000000, 1, 999999, 2],
}
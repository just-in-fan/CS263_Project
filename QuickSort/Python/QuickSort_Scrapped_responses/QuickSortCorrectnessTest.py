import QuickSort_ChatGPT_v1
import QuickSort_ChatGPT_v2
import QuickSort_ChatGPT_v3
import QuickSort_Claude
import QuickSort_DeepSeek_v1
import QuickSort_DeepSeek_v2
import QuickSort_Gemini

from typing import List
import random
random.seed(1)
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'algorithms'))

TEST_CASES = {
    "empty": [],
    "single_element": [5],
    "already_sorted": [1, 2, 3, 4, 5],
    "reverse_sorted": [5, 4, 3, 2, 1],
    "random_small": [random.randint(1, 10) for _ in range(5)],
    "random_large": [random.randint(1, 10000) for _ in range(1000)],
    "duplicates": [3, 1, 4, 1, 5, 9, 2, 6, 5],
    "negative_numbers": [-5, 2, -3, 0, -1, 4],
    "floating_point": [3.14, 1.41, 2.71, 0.0, -1.0],
    "edge_case_large_range": [1000000, 1, 999999, 2],
}

TEST_ANSWERS = {
    "empty": [],
    "single_element": [5],
    "already_sorted": [1, 2, 3, 4, 5],
    "reverse_sorted": [1, 2, 3, 4, 5],
    "random_small": sorted(TEST_CASES["random_small"]),
    "random_large": sorted(TEST_CASES["random_large"]),
    "duplicates": [1, 1, 2, 3, 4, 5, 5, 6, 9],
    "negative_numbers": [-5, -3, -1, 0, 2, 4],
    "floating_point": [-1.0, 0.0, 1.41, 2.71, 3.14],
    "edge_case_large_range": [1, 2, 999999, 1000000],
}

"""
class TestSortingCorrectness:

    def test_empty_array(self, sort_function):
        assert sort_function(TEST_CASES["empty"]) == []
    
    def test_single_element(self, sort_function):
        assert sort_function(TEST_CASES["single_element"]) == [5]
    
    def test_already_sorted(self, sort_function):
        assert sort_function(TEST_CASES["already_sorted"]) == [1, 2, 3, 4, 5]
    
    def test_reverse_sorted(self, sort_function):
        assert sort_function(TEST_CASES["reverse_sorted"]) == [1, 2, 3, 4, 5]
    
    def test_random_small(self, sort_function):
        assert sort_function(TEST_CASES["random_small"]) == sorted(TEST_CASES["random_small"])

    def test_large_random(self, sort_function):
        assert sort_function(TEST_CASES["random_large"]) == sorted(TEST_CASES["random_large"])

    def test_duplicates(self, sort_function):
        assert sort_function(TEST_CASES["duplicates"]) == [1, 1, 2, 3, 4, 5, 5, 6, 9]
    
    def test_negative_numbers(self, sort_function):
        assert sort_function(TEST_CASES["negative_numbers"]) == [-5, -3, -1, 0, 2, 4]
    
    def test_floating_point(self, sort_function):
        assert sort_function(TEST_CASES["floating_point"]) == [-1.0, 0.0, 1.41, 2.71, 3.14]

    def test_large_range(self, sort_function):
        assert sort_function(TEST_CASES["edge_case_large_range"]) == [1, 2, 999999, 1000000]
"""
        
# ChatGPT v1 
def ChatGPTv1(arr: List[int]) -> List[int]:
    """Return a new sorted list (not in-place)."""
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[len(arr) // 2]
    left  = [x for x in arr if x < pivot]
    mid   = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return ChatGPTv1(left) + mid + ChatGPTv1(right)

# ChatGPT v2
def ChatGPTv2_lomuto_partition(a: List[int], lo: int, hi: int) -> int:
    pivot = a[hi]
    i = lo
    for j in range(lo, hi):
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i

def ChatGPTv2_quicksort_inplace(a: List[int], lo: int = 0, hi: int | None = None) -> None:
    """Sort list 'a' in-place. Call with quicksort_inplace(a)."""
    if hi is None:
        hi = len(a) - 1
    if lo < hi:
        p = ChatGPTv2_lomuto_partition(a, lo, hi)
        ChatGPTv2_quicksort_inplace(a, lo, p - 1)
        ChatGPTv2_quicksort_inplace(a, p + 1, hi)

# ChatGPT v3
def ChatGPTv3_randomized_partition(a: List[int], lo: int, hi: int) -> int:
    pivot_idx = random.randint(lo, hi)
    a[pivot_idx], a[hi] = a[hi], a[pivot_idx]
    # reuse Lomuto partition
    pivot = a[hi]
    i = lo
    for j in range(lo, hi):
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i

def ChatGPTv3_quicksort_randomized(a: List[int], lo: int = 0, hi: int | None = None) -> None:
    if hi is None:
        hi = len(a) - 1
    if lo < hi:
        p = ChatGPTv3_randomized_partition(a, lo, hi)
        ChatGPTv3_quicksort_randomized(a, lo, p - 1)
        ChatGPTv3_quicksort_randomized(a, p + 1, hi)

# Claude
def Claude(arr):
    """
    Sorts an array using the quicksort algorithm.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        Sorted list
    """
    # Base case: arrays with 0 or 1 element are already sorted
    if len(arr) <= 1:
        return arr
    
    # Choose pivot (using middle element for better average performance)
    pivot = arr[len(arr) // 2]
    
    # Partition array into three parts
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    # Recursively sort left and right partitions
    return Claude(left) + middle + Claude(right)

# DeepSeek_v1 (same as Claude)
def DeepSeekv1(arr):
    """
    Sorts an array using the quicksort algorithm.
    
    Args:
        arr: List of comparable elements
        
    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]  # Choose middle element as pivot
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return DeepSeekv1(left) + middle + DeepSeekv1(right)

# DeepSeek_v2
def DeepSeekv2_quicksort_inplace(arr, low=0, high=None):
    """
    In-place quicksort implementation.
    
    Args:
        arr: List to be sorted
        low: Starting index
        high: Ending index
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Partition the array and get the pivot index
        pivot_index = DeepSeekv2_partition(arr, low, high)
        
        # Recursively sort elements before and after partition
        DeepSeekv2_quicksort_inplace(arr, low, pivot_index - 1)
        DeepSeekv2_quicksort_inplace(arr, pivot_index + 1, high)

def DeepSeekv2_partition(arr, low, high):
    """
    Partitions the array around a pivot element.
    
    Args:
        arr: List to partition
        low: Starting index
        high: Ending index
        
    Returns:
        Index of the pivot after partitioning
    """
    # Choose the rightmost element as pivot
    pivot = arr[high]
    
    # Index of smaller element (indicates right position of pivot)
    i = low - 1
    
    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Swap elements
    
    # Place the pivot in the correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# Gemini
def Gemini(arr):
  """
  Sorts a list in ascending order using the Quicksort algorithm.
  """
  if len(arr) <= 1:
    # Base case: A list with 0 or 1 element is already sorted
    return arr
  else:
    # 1. Choose a pivot element
    # We'll use the first element as the pivot.
    pivot = arr[0]
    
    # 2. Partition the list
    # Create two sub-lists: one for elements less than or equal to the pivot,
    # and one for elements greater than the pivot.
    # We use list slicing (arr[1:]) to iterate over elements *other* than the pivot.
    
    less = [x for x in arr[1:] if x <= pivot]
    greater = [x for x in arr[1:] if x > pivot]
    
    # 3. Recurse
    # Recursively sort the sub-lists and combine them with the pivot in the middle.
    return Gemini(less) + [pivot] + Gemini(greater)

def run_test_case(sort_function, test_name, test_input, expected_output, is_inplace=False):
    """
    Run a single test case for a given sorting function
    """
    try:
        # Handle in-place vs return-new-array functions
        if is_inplace:
            # For in-place functions, we need to copy the input first
            test_copy = test_input.copy()
            sort_function(test_copy)
            result = test_copy
        else:
            # For functions that return a new array
            result = sort_function(test_input)
        
        # Check if result matches expected output
        if result == expected_output:
            return True, None
        else:
            return False, f"Expected {expected_output}, got {result}"
            
    except Exception as e:
        return False, f"Exception: {str(e)}"

def run_all_tests_for_function(sort_function, function_name, is_inplace=False):
    """
    Run all test cases for a single sorting function
    """
    print(f"\n{'='*60}")
    print(f"Testing {function_name}")
    print(f"{'='*60}")
    
    results = {}
    passed = 0
    total = len(TEST_CASES)
    
    for test_name, test_input in TEST_CASES.items():
        expected_output = TEST_ANSWERS[test_name]
        
        success, message = run_test_case(sort_function, test_name, test_input, expected_output, is_inplace)
        
        if success:
            print(f"{test_name:20} PASSED")
            passed += 1
        else:
            print(f"{test_name:20} FAILED - {message}")
        
        results[test_name] = {
            'success': success,
            'message': message,
            'input': test_input,
            'expected': expected_output,
            'actual': message if not success else "PASSED"
        }
    
    print(f"\n {function_name} Summary: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    return results, passed, total

def main():
    """
    Main function to run all tests for all sorting algorithms
    """
    # Define all functions to test with their properties
    functions_to_test = [
        # (function, name, is_inplace)
        (ChatGPTv1, "ChatGPT_v1", False),
        (Claude, "Claude", False),
        (DeepSeekv1, "DeepSeek_v1", False),
        (Gemini, "Gemini", False),
        
        # In-place functions need special handling
        (lambda arr: ChatGPTv2_quicksort_inplace(arr) or arr, "ChatGPT_v2", True),
        (lambda arr: ChatGPTv3_quicksort_randomized(arr) or arr, "ChatGPT_v3", True),
        (lambda arr: DeepSeekv2_quicksort_inplace(arr) or arr, "DeepSeek_v2", True),
    ]
    
    overall_results = {}
    total_passed = 0
    total_tests = 0
    
    print("Starting QuickSort Algorithm Benchmark")
    print("=" * 60)
    
    # Test each function
    for sort_func, func_name, is_inplace in functions_to_test:
        results, passed, total = run_all_tests_for_function(sort_func, func_name, is_inplace)
        overall_results[func_name] = results
        total_passed += passed
        total_tests += total
    
    # Print final summary
    print("\n" + "=" * 60)
    print("FINAL RESULTS SUMMARY")
    print("=" * 60)
    
    for func_name in overall_results:
        passed_count = sum(1 for test in overall_results[func_name].values() if test['success'])
        total_count = len(overall_results[func_name])
        percentage = (passed_count / total_count) * 100
        print(f"{func_name:15} {passed_count:2d}/{total_count:2d} ({percentage:6.1f}%)")
    
    print(f"\nOverall: {total_passed}/{total_tests} tests passed "
          f"({total_passed/total_tests*100:.1f}%)")

if __name__ == "__main__":
    main()
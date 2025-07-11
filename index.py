"""
Divide and Conquer Algorithms: Merge Sort vs Quick Sort

Author: AJAL RC (Student ID: 005039456)
Course: Algorithms and Data Structures (MSCS-532-B01)
Assignment 2: Analyzing and Implementing Divide-and-Conquer Algorithms

Description:
-------------
This script implements and compares two classic divide-and-conquer sorting algorithms:
    1. Merge Sort
    2. Quick Sort

It benchmarks their performance (execution time and memory usage) on different types
of input data (random, sorted, and reverse sorted arrays) for various array sizes.

The script outputs timing and memory consumption for each case, enabling a practical
comparison with theoretical expectations.

"""

import random           # Used for generating random arrays
import time             # Used for measuring execution time
import tracemalloc      # Used for tracking memory usage
import sys              # Used for setting recursion limit (for large arrays)

# -- Merge Sort Implementation --
def merge_sort(arr):
    """
    Sorts an array in ascending order using the merge sort algorithm.
    This function modifies the array in place.

    Args:
        arr (list): List of comparable elements (e.g., integers).

    Returns:
        None
    """
    # Base case: If array has 0 or 1 element, it's already sorted
    if len(arr) <= 1:
        return

    # Find the middle index to divide the array into halves
    mid = len(arr) // 2
    left_half = arr[:mid]      # Copy left half
    right_half = arr[mid:]     # Copy right half

    # Recursively sort both halves
    merge_sort(left_half)
    merge_sort(right_half)

    # Merge two sorted halves into the original array
    i = j = k = 0  # i for left_half, j for right_half, k for arr

    # Compare elements from left and right halves, copy smallest back to arr
    while i < len(left_half) and j < len(right_half):
        if left_half[i] <= right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k += 1

    # Copy any remaining elements from left_half, if any
    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1

    # Copy any remaining elements from right_half, if any
    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1

# -- Quick Sort Implementation --
def quick_sort(arr):
    """
    Sorts an array in ascending order using the quick sort algorithm.
    This function modifies the array in place.

    Args:
        arr (list): List of comparable elements (e.g., integers).

    Returns:
        None
    """

    def _quick_sort(items, low, high):
        """
        Recursive helper function for quick sort.

        Args:
            items (list): The array to sort.
            low (int): The starting index of the array segment.
            high (int): The ending index of the array segment.
        """
        # Base case: segment of one or zero elements is already sorted
        if low < high:
            # Partition the array and get the index of the pivot
            pi = partition(items, low, high)
            # Recursively sort elements before and after partition
            _quick_sort(items, low, pi - 1)
            _quick_sort(items, pi + 1, high)

    def partition(items, low, high):
        """
        Partitions the array for quick sort using the last element as the pivot.

        Args:
            items (list): The array to partition.
            low (int): The starting index.
            high (int): The ending index.

        Returns:
            int: The index position of the pivot.
        """
        pivot = items[high]  # Select last element as pivot
        i = low - 1          # i will mark end of "smaller than pivot" region
        for j in range(low, high):
            if items[j] <= pivot:
                i += 1
                # Swap current element with element at i
                items[i], items[j] = items[j], items[i]
        # Place the pivot after the last smaller element
        items[i + 1], items[high] = items[high], items[i + 1]
        return i + 1

    # Call the recursive helper on the full array
    _quick_sort(arr, 0, len(arr) - 1)

# -- Data Generation Utility --
def generate_data(n, data_type="random"):
    """
    Generates an array of specified size and data pattern.

    Args:
        n (int): Size of the array.
        data_type (str): Type of data pattern: "random", "sorted", "reverse".

    Returns:
        list: Generated array.
    """
    if data_type == "random":
        # Create random integers between 1 and n (inclusive)
        return [random.randint(1, n) for _ in range(n)]
    elif data_type == "sorted":
        # Create a sorted array
        return list(range(n))
    elif data_type == "reverse":
        # Create a reverse-sorted array
        return list(range(n, 0, -1))
    else:
        raise ValueError("Unsupported data type: choose 'random', 'sorted', or 'reverse'.")

# -- Performance Measurement Utility --
def measure_performance(sort_func, data):
    """
    Measures the execution time and memory usage of a sorting function.

    Args:
        sort_func (function): Sorting function to benchmark.
        data (list): The array to sort.

    Returns:
        tuple: (execution time in seconds, peak memory usage in KB)
    """
    tracemalloc.start()                      # Start memory tracking
    start_time = time.perf_counter()         # Start the timer
    sort_func(data)                          # Run the sort
    end_time = time.perf_counter()           # End the timer
    current, peak = tracemalloc.get_traced_memory()  # Get memory info
    tracemalloc.stop()                       # Stop memory tracking
    return end_time - start_time, peak / 1024  # Return time and memory in KB

# -- Main Benchmarking Logic --
if __name__ == "__main__":
    # Set a safe recursion limit for sorting moderately large arrays
    sys.setrecursionlimit(10000)

    # Define array sizes and data types to test
    sizes = [1000, 3000]
    data_types = ["random", "sorted", "reverse"]

    for n in sizes:
        print(f"\n Please wait. The data is getting sorted for Array size {n}")
        for dtype in data_types:
            # Generate test data for this size/type
            arr1 = generate_data(n, dtype)
            arr2 = list(arr1)  # Make a separate copy for the second algorithm

            # Measure Merge Sort
            t_merge, mem_merge = measure_performance(merge_sort, arr1)

            # Measure Quick Sort
            t_quick, mem_quick = measure_performance(quick_sort, arr2)

            # Print performance metrics, formatted for readability
            print(f"  Data: {dtype:<8} | Merge Sort: {t_merge:.4f}s, {mem_merge:.1f}KB | "
                  f"Quick Sort: {t_quick:.4f}s, {mem_quick:.1f}KB")

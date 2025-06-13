#!/usr/bin/env python3

def bubble_sort(arr):
    """
    Sorts an array using the bubble sort algorithm.

    Time Complexity: O(n^2)
    Space Complexity: O(1)

    :param arr: List of elements to be sorted
    :return: Sorted list
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def quick_sort(arr):
    """
    Sorts an array using the quick sort algorithm.

    Time Complexity: O(n log n) on average
    Space Complexity: O(n)

    :param arr: List of elements to be sorted
    :return: Sorted list
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

if __name__ == "__main__":
    # Example usage
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    
    # Test bubble sort
    bubble_sorted = bubble_sort(test_array.copy())
    print("Bubble sorted:", bubble_sorted)
    
    # Test quick sort
    quick_sorted = quick_sort(test_array.copy())
    print("Quick sorted:", quick_sorted)
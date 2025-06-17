#!/usr/bin/env python3

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def selection_sort(arr):
    """
    Sorts an array using the selection sort algorithm.

    Selection sort divides the input list into two parts: a sorted sublist of items 
    which is built up from left to right at the front (left) of the list and a sublist 
    of the remaining unsorted items. It repeatedly selects the minimum element from 
    the unsorted portion, swapping it into the correct sorted position.

    Time Complexity:
        Best, Average, Worst: O(n^2)
    Space Complexity:
        O(1) - in-place sorting

    Example:
        arr = [64, 34, 25, 12, 22, 11, 90]
        sorted_arr = selection_sort(arr)
        print(sorted_arr)  # [11, 12, 22, 25, 34, 64, 90]
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

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

    # Test selection sort
    selection_sorted = selection_sort(test_array.copy())
    print("Selection sorted:", selection_sorted)
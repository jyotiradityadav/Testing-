#!/usr/bin/env python3

def bubble_sort(arr):
    """
    Sorts an array using the bubble sort algorithm.
    
    Args:
        arr: List of comparable elements to be sorted
        
    Returns:
        The sorted list
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

if __name__ == "__main__":
    # Example usage
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    
    # Test bubble sort
    sorted_array = bubble_sort(test_array.copy())
    print("Bubble sorted:", sorted_array)
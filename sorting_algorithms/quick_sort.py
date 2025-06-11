def quick_sort(arr):
    """
    Quick Sort implementation
    Time Complexity: O(n log n) average case, O(n^2) worst case
    Space Complexity: O(log n)
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

# Example usage
if __name__ == "__main__":
    # Test the quick sort
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    sorted_array = quick_sort(test_array)
    print("Sorted array:", sorted_array) 
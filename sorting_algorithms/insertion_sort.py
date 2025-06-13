def bubble_sort(arr):
    """
    Bubble Sort implementation
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    n = len(arr)
    for i in range(n):
        # Track if any elements were swapped in this pass
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        # If no elements were swapped, the array is sorted
        if not swapped:
            break
    return arr

# Example usage
if __name__ == "__main__":
    # Test the bubble sort
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    sorted_array = bubble_sort(test_array.copy())
    print("Sorted array:", sorted_array)
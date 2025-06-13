def bubble_sort(arr):
    """
    Bubble Sort implementation
    Time Complexity: O(n^2) in all cases
    Space Complexity: O(1)
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

# Example usage
if __name__ == "__main__":
    # Test the bubble sort
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    bubble_sort(test_array)
    print("Sorted array:", test_array)
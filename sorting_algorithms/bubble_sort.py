def bubble_sort(arr):
    """
    Bubble Sort implementation
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    n = len(arr)
    for i in range(n):
        # Flag to optimize if no swaps occur
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        
        # If no swapping occurred, array is sorted
        if not swapped:
            break
    
    return arr

# Example usage
if __name__ == "__main__":
    # Test the bubble sort
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    sorted_array = bubble_sort(test_array)
    print("Sorted array:", sorted_array) 
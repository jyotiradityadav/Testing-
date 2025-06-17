def bubble_sort(arr):
    """
    Bubble Sort implementation
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    if len(arr) <= 1:
        return arr
    
    # Create a copy to avoid modifying the original array
    arr_copy = arr.copy()
    n = len(arr_copy)
    
    # Traverse through all array elements
    for i in range(n):
        # Flag to optimize - if no swapping occurs, array is sorted
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater than the next element
            if arr_copy[j] > arr_copy[j + 1]:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                swapped = True
        
        # If no two elements were swapped, then the array is sorted
        if not swapped:
            break
    
    return arr_copy

# Example usage
if __name__ == "__main__":
    # Test the bubble sort
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    sorted_array = bubble_sort(test_array)
    print("Sorted array:", sorted_array)
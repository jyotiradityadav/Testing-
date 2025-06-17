def bubble_sort(arr):
    """
    Sorts an array using the bubble sort algorithm.
    
    Args:
        arr: List of comparable elements to be sorted
        
    Returns:
        List: The sorted array
        
    Example:
        >>> bubble_sort([64, 34, 25, 12, 22, 11, 90])
        [11, 12, 22, 25, 34, 64, 90]
    """
    n = len(arr)
    
    # Traverse through all array elements
    for i in range(n):
        # Flag to optimize - if no swapping occurs, array is sorted
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no two elements were swapped, then the array is sorted
        if not swapped:
            break
    
    return arr


if __name__ == "__main__":
    # Example usage
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    
    sorted_array = bubble_sort(test_array.copy())
    print("Sorted array:", sorted_array)
    
    # Test with edge cases
    print("
Edge cases:")
    print("Empty array:", bubble_sort([]))
    print("Single element:", bubble_sort([42]))
    print("Already sorted:", bubble_sort([1, 2, 3, 4, 5]))
    print("Reverse sorted:", bubble_sort([5, 4, 3, 2, 1]))
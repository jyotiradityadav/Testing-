def insertion_sort(arr):
    """
    Insertion Sort implementation
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Move elements that are greater than key
        # to one position ahead of their current position
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr

# Example usage
if __name__ == "__main__":
    # Test the insertion sort
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    sorted_array = insertion_sort(test_array)
    print("Sorted array:", sorted_array) 
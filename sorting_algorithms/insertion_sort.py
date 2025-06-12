def insertion_sort(arr):
    """
    Sorts a list of elements in ascending order using the Insertion Sort algorithm.

    Insertion Sort is an in-place, comparison-based sorting algorithm. 
    It builds the sorted array one item at a time by repeatedly picking 
    the next element and inserting it into the correct position in the already sorted part.

    Time Complexity:
        Worst-case: O(n^2)   (when the array is reverse sorted)
        Best-case:  O(n)     (when the array is already sorted)
        Average:    O(n^2)

    Space Complexity: O(1)   (sorts in-place)

    Parameters:
        arr (list): The list of elements to sort. Elements must be comparable.

    Returns:
        list: The sorted list (the sorting is performed in-place, 
              but the reference is returned for convenience).

    Example:
        >>> arr = [5, 2, 9, 1, 5]
        >>> insertion_sort(arr)
        [1, 2, 5, 5, 9]
    """
    # Traverse through the array starting from the second element
    for i in range(1, len(arr)):
        key = arr[i]      # Element to be positioned
        j = i - 1

        # Shift elements of arr[0..i-1], that are greater than key,
        # to one position ahead of their current position
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]  # Move the greater element one position up
            j -= 1

        # Insert the 'key' at the correct position found
        arr[j + 1] = key

    return arr

# Example usage
if __name__ == "__main__":
    # Test the insertion sort with a sample array
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    sorted_array = insertion_sort(test_array)
    print("Sorted array:", sorted_array)
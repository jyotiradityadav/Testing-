"""
Module: insertion_sort
----------------------
Provides an implementation of the insertion sort algorithm for sorting lists in-place.

Author: (Insert Author Name)
Date: (Insert Date)
"""

def insertion_sort(arr):
    """
    Sorts a list in ascending order using the insertion sort algorithm.

    The algorithm iterates through the list, and for each element, inserts it into its correct
    position within the sorted portion of the list (to the left of the current index).

    Parameters
    ----------
    arr : list
        The list of comparable elements to be sorted in place. The list is modified directly.

    Returns
    -------
    list
        The sorted list (the original reference).

    Time Complexity
    ---------------
    Best case:    O(n)      (already sorted)
    Average case: O(n^2)
    Worst case:   O(n^2)

    Space Complexity
    ----------------
    O(1)  (in-place)

    Example
    -------
    >>> a = [5, 3, 1, 4, 2]
    >>> insertion_sort(a)
    [1, 2, 3, 4, 5]
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # Shift elements of arr[0..i-1] that are greater than key one position to the right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        # Place key at the correct location
        arr[j + 1] = key

    return arr

if __name__ == "__main__":
    # Example usage: sort an array and display results
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    sorted_array = insertion_sort(test_array)
    print("Sorted array:", sorted_array)
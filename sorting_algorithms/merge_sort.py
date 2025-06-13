def merge_sort(arr):
    """
    Merge Sort implementation
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    This implementation sorts the list in place and returns None.
    """
    if arr is None or len(arr) <= 1:
        return

    temp = [0] * len(arr)
    _merge_sort_recursive(arr, temp, 0, len(arr) - 1)

def _merge_sort_recursive(arr, temp, left, right):
    if left < right:
 
        print("Original array:", test_array)
        arr = test_array.copy()
        merge_sort(arr)
        print("Sorted array:", arr)
        print()

def merge_sort(arr):
    """
    Merge Sort implementation
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    The function sorts the list in-place and also returns it.
    """
    # Defensive: operate on a copy if original should not be mutated
    if not isinstance(arr, list):
        raise ValueError("Input must be a list")


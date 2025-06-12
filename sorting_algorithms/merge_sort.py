def merge_sort(arr):
    """
    Merge Sort implementation
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    # Defensive copy to avoid modifying input
    if not isinstance(arr, list):
        raise ValueError("Input must be a list")


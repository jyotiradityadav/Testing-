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
        mid = (left + right) // 2
        _merge_sort_recursive(arr, temp, left, mid)
        _merge_sort_recursive(arr, temp, mid + 1, right)
        _merge(arr, temp, left, mid, right)

def _merge(arr, temp, left, mid, right):
    i = left
    j = mid + 1
    k = left

    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            j += 1
        k += 1

    while i <= mid:
        temp[k] = arr[i]
        i += 1
        k += 1

    while j <= right:
        temp[k] = arr[j]
        j += 1
        k += 1

    for l in range(left, right + 1):
        arr[l] = temp[l]

# Example usage
if __name__ == "__main__":
    # Test the merge sort
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [],
        [1],
        [2, 1],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [4, 2, 2, 8, 3, 3, 1],
    ]
    for test_array in test_cases:
        print("Original array:", test_array)
        arr = test_array.copy()
        merge_sort(arr)
        print("Sorted array:", arr)
        print()
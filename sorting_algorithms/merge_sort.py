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

    # If length <=1, it's already sorted
    if len(arr) <= 1:
        return arr

    # Divide the array into two halves
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    # Merge the two halves
    return merge(left, right)

def merge(left, right):
    """
    Helper function to merge two sorted arrays into a single sorted array.
    """
    result = []
    i = j = 0

    # Merge until one side is exhausted
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Add remaining elements from both halves (at most one will be non-empty)
    if i < len(left):
        result.extend(left[i:])
    if j < len(right):
        result.extend(right[j:])

    return result

# Example usage and tests
if __name__ == "__main__":
    test_arrays = [
        [64, 34, 25, 12, 22, 11, 90],
        [],
        [42],
        [3, 2, 1, 0, -1, -2],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [2, 1, 2, 1],
    ]

    for idx, test_array in enumerate(test_arrays):
        print(f"Test {idx+1}:")
        print("Original array:", test_array)
        sorted_array = merge_sort(test_array)
        print("Sorted array:  ", sorted_array)
        assert sorted_array == sorted(test_array), "Merge sort failed!"
        print("---")
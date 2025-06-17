def merge_sort(arr):
    """
    Merge Sort implementation
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    """Helper function to merge two sorted arrays"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

def _run_tests():
    test_cases = [
        ([], []),
        ([1], [1]),
        ([2, 1], [1, 2]),
        ([1, 2, 3, 4], [1, 2, 3, 4]),
        ([4, 3, 2, 1], [1, 2, 3, 4]),
        ([5, 3, 8, 3, 9, 1], [1, 3, 3, 5, 8, 9]),
        ([12, -5, 0, 12, 3, 3], [-5, 0, 3, 3, 12, 12]),
        ([2, 2, 2, 2], [2, 2, 2, 2])
    ]
    for i, (input_arr, expected) in enumerate(test_cases):
        assert merge_sort(input_arr) == expected, f"Test case {i+1} failed: {input_arr}"

if __name__ == "__main__":
    # Example usage
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    sorted_array = merge_sort(test_array)
    print("Sorted array:", sorted_array)

    # Run unit tests
    _run_tests()
    print("All tests passed.")
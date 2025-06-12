def merge_sort(arr):
    """
    Merge Sort implementation
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    # Defensive copy to avoid modifying input
    if not isinstance(arr, list):
        raise ValueError("Input must be a list")

    if len(arr) <= 1:
        return arr[:]

    # Divide the array into two halves
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    # Merge the two halves
    return merge(left, right)

def merge(left, right):
    """Helper function to merge two sorted arrays"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # Ascending order
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])

    return result

# In-place variant for users expecting `arr` to be sorted in place
def merge_sort_inplace(arr):
    """
    Sorts the array in place using merge sort.
    """
    sorted_arr = merge_sort(arr)
    for i in range(len(arr)):
        arr[i] = sorted_arr[i]

# Example usage and tests
if __name__ == "__main__":
    # Test the merge sort
    test_cases = [
        [],
        [1],
        [2, 1],
        [64, 34, 25, 12, 22, 11, 90],
        [5, -1, 3, 9, 0, 2],
        [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ]
    for test_array in test_cases:
        print("Original array:", test_array)
        sorted_array = merge_sort(test_array)
        print("Sorted array (copy):", sorted_array)
        assert sorted_array == sorted(test_array), f"Test failed for {test_array}"
        # In-place sort
        arr_inplace = test_array[:]
        merge_sort_inplace(arr_inplace)
        print("Sorted array (in-place):", arr_inplace)
        assert arr_inplace == sorted(test_array), f"In-place test failed for {test_array}"
        print("---")

---
This is how this task will be automated :
- Step 1: Carefully review and correct the recursive logic so the original array is not mutated and result is always correct.
- Step 2: Add defensive checks and an in-place variant for convenience.
- Step 3: Implement comprehensive testing in the main block to ensure correct sorting in all scenarios (empty, one element, multiple elements, negatives, already sorted, reverse sorted, etc.).
- Step 4: Validate output and correctness via assertions.
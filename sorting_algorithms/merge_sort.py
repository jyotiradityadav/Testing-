def merge_sort(arr):
    """
    Merge Sort implementation.
    Sorts an array in ascending order using the Merge Sort algorithm.

    Algorithm:
        - Recursively divide the array into halves until one element in each.
        - Merge the sorted halves into a single sorted array.

    Time Complexity: O(n log n)
    Space Complexity: O(n)

    Example:
        >>> merge_sort([4, 3, 1, 2])
        [1, 2, 3, 4]
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    """Helper function to merge two sorted arrays."""
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

if __name__ == "__main__":
    # Test the merge sort
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    sorted_array = merge_sort(test_array)
    print("Sorted array:", sorted_array)
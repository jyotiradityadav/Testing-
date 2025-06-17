def merge_sort(arr):
    """
    Merge Sort implementation
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if len(arr) <= 1:
        return arr

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
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

# Example usage and test cases
if __name__ == "__main__":
    test_cases = [
        [],
        [1],
        [2, 1],
        [5, 3, 8, 4, 2],
        [64, 34, 25, 12, 22, 11, 90],
        [3, 3, 3, 3],
        [-1, -3, 0, 2, -5, 8],
        [10, -2, 0, 5, 5, -2, 10]
    ]
    for idx, test_array in enumerate(test_cases):
        print(f"Test case {idx+1}: Original array: {test_array}")
        sorted_array = merge_sort(test_array)
        print(f"Sorted array: {sorted_array}
")
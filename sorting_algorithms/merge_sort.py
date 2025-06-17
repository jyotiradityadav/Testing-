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

    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])

    return result

# Example usage and basic tests
if __name__ == "__main__":
    # Test the merge sort
    test_cases = [
        [],
        [1],
        [2, 1],
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 2, 5, 1],
        [-1, -3, 2, 0, -2, 5, 5, -3]
    ]
    for idx, test_array in enumerate(test_cases):
        print(f"Test case #{idx + 1}:")
        print("Original array:", test_array)
        sorted_array = merge_sort(test_array)
        print("Sorted array:  ", sorted_array)
        print("-" * 30)
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
        if left[i] <= right[j]:  # Fix: sort in ascending order
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])

    return result

# Example usage
if __name__ == "__main__":
    # Test the merge sort
    test_cases = [
        [],
        [1],
        [3, 1, 2],
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 9, 1, 5, 6],
        [-3, -1, -2, -5, 0],
        [2, 2, 2, 2, 2],
    ]
    for test_array in test_cases:
        print("Original array:", test_array)
        sorted_array = merge_sort(test_array)
        print("Sorted array:", sorted_array)
def merge_sort(arr):
    """
    Merge Sort implementation
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Args:
        arr: List of comparable elements to be sorted
        
    Returns:
        List: A new sorted list containing all elements from input array
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
    """
    Helper function to merge two sorted arrays
    
    Args:
        left: First sorted array
        right: Second sorted array
        
    Returns:
        List: Merged sorted array containing all elements from both input arrays
    """
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

def test_merge_sort():
    """Unit tests for merge sort implementation"""
    
    # Test empty array
    assert merge_sort([]) == []
    
    # Test single element
    assert merge_sort([1]) == [1]
    
    # Test already sorted array
    assert merge_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    
    # Test reverse sorted array
    assert merge_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    
    # Test array with duplicates
    assert merge_sort([3, 1, 4, 1, 5, 9, 2, 6, 5]) == [1, 1, 2, 3, 4, 5, 5, 6, 9]
    
    # Test array with negative numbers
    assert merge_sort([-3, -1, -4, 1, 5, -9, 2]) == [-9, -4, -3, -1, 1, 2, 5]
    
    # Test array with mixed positive and negative numbers
    assert merge_sort([0, -1, 1, -2, 2]) == [-2, -1, 0, 1, 2]
    
    # Test large array
    import random
    large_array = [random.randint(1, 1000) for _ in range(100)]
    sorted_large = merge_sort(large_array)
    assert sorted_large == sorted(large_array)
    
    print("All tests passed!")

# Example usage
if __name__ == "__main__":
    # Test the merge sort
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    sorted_array = merge_sort(test_array)
    print("Sorted array:", sorted_array)
    
    # Run unit tests
    test_merge_sort()
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

if __name__ == "__main__":
    import unittest

    class TestMergeSort(unittest.TestCase):
        def test_empty(self):
            self.assertEqual(merge_sort([]), [])

        def test_single_element(self):
            self.assertEqual(merge_sort([1]), [1])

        def test_sorted(self):
            self.assertEqual(merge_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

        def test_reverse_sorted(self):
            self.assertEqual(merge_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

        def test_duplicates(self):
            self.assertEqual(merge_sort([3, 1, 2, 3, 1]), [1, 1, 2, 3, 3])

        def test_mixed(self):
            self.assertEqual(merge_sort([64, 34, 25, 12, 22, 11, 90]), [11, 12, 22, 25, 34, 64, 90])

    unittest.main()
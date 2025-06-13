# Sorting Algorithms Time Complexity

Sorting algorithms are fundamental in computer science, used to arrange data in a particular order. Understanding their time complexity is crucial for selecting the appropriate algorithm based on the data size and requirements. Below is an analysis of several common sorting algorithms, focusing on their time complexities.

## 1. Bubble Sort

### Description
Bubble Sort is a simple comparison-based algorithm. It repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. This process is repeated until the list is sorted.

### Time Complexity
- **Best Case:** O(n) - Occurs when the list is already sorted.
- **Average Case:** O(n²)
- **Worst Case:** O(n²) - Occurs when the list is sorted in reverse order.

## 2. Selection Sort

### Description
Selection Sort divides the list into a sorted and an unsorted region. It repeatedly selects the smallest (or largest, depending on sorting order) element from the unsorted region and moves it to the end of the sorted region.

### Time Complexity
- **Best Case:** O(n²)
- **Average Case:** O(n²)
- **Worst Case:** O(n²)

## 3. Insertion Sort

### Description
Insertion Sort builds the sorted array one item at a time. It takes each element from the input and finds the correct position within the sorted part of the array.

### Time Complexity
- **Best Case:** O(n) - Occurs when the list is already sorted.
- **Average Case:** O(n²)
- **Worst Case:** O(n²)

## 4. Merge Sort

### Description
Merge Sort is a divide-and-conquer algorithm. It divides the list into two halves, recursively sorts them, and then merges the sorted halves.

### Time Complexity
- **Best Case:** O(n log n)
- **Average Case:** O(n log n)
- **Worst Case:** O(n log n)

## 5. Quick Sort

### Description
Quick Sort is another divide-and-conquer algorithm. It selects a 'pivot' element and partitions the array into two sub-arrays according to whether they are less than or greater than the pivot. It then recursively sorts the sub-arrays.

### Time Complexity
- **Best Case:** O(n log n)
- **Average Case:** O(n log n)
- **Worst Case:** O(n²) - Occurs when the smallest or largest element is always chosen as the pivot.

## 6. Heap Sort

### Description
Heap Sort is a comparison-based algorithm that uses a binary heap data structure. It builds a max heap and then repeatedly extracts the maximum element from the heap and rebuilds the heap.

### Time Complexity
- **Best Case:** O(n log n)
- **Average Case:** O(n log n)
- **Worst Case:** O(n log n)

## 7. Counting Sort

### Description
Counting Sort is a non-comparison-based algorithm. It counts the number of occurrences of each distinct element and uses this information to place each element in its correct position.

### Time Complexity
- **Best Case:** O(n + k)
- **Average Case:** O(n + k)
- **Worst Case:** O(n + k)
- **Note:** `k` is the range of the input.

## 8. Radix Sort

### Description
Radix Sort is a non-comparison-based algorithm that sorts numbers by processing individual digits. It uses Counting Sort as a subroutine to sort the digits.

### Time Complexity
- **Best Case:** O(nk)
- **Average Case:** O(nk)
- **Worst Case:** O(nk)
- **Note:** `k` is the number of digits in the largest number.

## Conclusion

The choice of sorting algorithm depends on the specific requirements and constraints of the problem, such as the size of the data set, the nature of the data, and the importance of stability. Understanding the time complexity of each algorithm helps in making an informed decision to optimize performance.
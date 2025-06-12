def selection_sort_recursive(arr, start=0):
    # Base case: If the start index is the last element, sorting is done
    if start >= len(arr) - 1:
        return arr

    # Find the minimum element in the unsorted portion
    min_index = start
    for i in range(start + 1, len(arr)):
        if arr[i] < arr[min_index]:
            min_index = i

    # Swap the found minimum element with the first unsorted element
    arr[start], arr[min_index] = arr[min_index], arr[start]

    # Recursively sort the remaining array
    return selection_sort_recursive(arr, start + 1)

if __name__ == "__main__":
    # Example usage
    arr = [64, 25, 12, 22, 11]
    print("Sorted array:", selection_sort_recursive(arr))

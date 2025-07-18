def selection_sort_iterative(arr):
    n = len(arr)
    for i in range(n - 1):
        # Find the minimum element in the unsorted portion
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j

        # Swap the found minimum element with the first unsorted element
        arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr

if __name__ == "__main__":
    # Example usage
    arr = [64, 25, 12, 22, 11]
    print("Sorted array:", selection_sort_iterative(arr))

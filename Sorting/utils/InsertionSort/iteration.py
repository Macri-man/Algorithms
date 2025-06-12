def insertion_sort_iterative(arr,capture):
    # Traverse from the second element to the last
    for i in range(1, len(arr)):
        key = arr[i]  # Current element to be placed
        j = i - 1

        # Shift elements of the sorted portion to the right to make room for the key
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        # Place the key at its correct position
        arr[j + 1] = key
        capture(arr)

    return arr
if __name__ == "__main__":
    # Example usage
    arr = [12, 11, 13, 5, 6]
    print("Sorted array:", insertion_sort_iterative(arr))

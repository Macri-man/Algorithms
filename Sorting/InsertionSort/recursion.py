def insertion_sort_recursive(arr, n=None):
    if n is None:
        n = len(arr)

    # Base case: If the array has 1 or fewer elements, it's already sorted
    if n <= 1:
        return arr

    # Sort the first n-1 elements
    insertion_sort_recursive(arr, n - 1)

    # Insert the last element of the current portion into the sorted part
    key = arr[n - 1]
    j = n - 2

    # Shift elements to make room for the key
    while j >= 0 and arr[j] > key:
        arr[j + 1] = arr[j]
        j -= 1

    arr[j + 1] = key

    return arr

if __name__ == "__main__":
    # Example usage
    arr = [12, 11, 13, 5, 6]
    print("Sorted array:", insertion_sort_recursive(arr))

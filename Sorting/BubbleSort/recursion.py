def bubble_sort_recursive(arr, n=None):
    if n is None:
        n = len(arr)
    # Base case: If the size of the array is 1
    if n == 1:
        return arr

    # Perform one pass of bubble sort
    for i in range(n - 1):
        if arr[i] > arr[i + 1]:
            arr[i], arr[i + 1] = arr[i + 1], arr[i]

    # Recursive call for the rest of the array
    return bubble_sort_recursive(arr, n - 1)

if __name__ == "__main__":
    # Example usage
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("Sorted array:", bubble_sort_recursive(arr))

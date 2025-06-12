def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1  # Index for smaller element

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort_recursive(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low < high:
        pi = partition(arr, low, high)

        # Recursively sort the subarrays
        quick_sort_recursive(arr, low, pi - 1)
        quick_sort_recursive(arr, pi + 1, high)

    return arr

if __name__ == "__main__":
    # Example usage
    arr = [10, 7, 8, 9, 1, 5]
    print("Sorted array:", quick_sort_recursive(arr))

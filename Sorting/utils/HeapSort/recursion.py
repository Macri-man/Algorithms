def heapify_recursive(arr, n, i):
    largest = i  # Initialize largest as root
    left = 2 * i + 1  # Left child
    right = 2 * i + 2  # Right child

    # Check if left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Check if right child exists and is greater than the largest so far
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If the largest is not root, swap and continue heapifying
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify_recursive(arr, n, largest)

def heap_sort_recursive(arr):
    n = len(arr)

    # Helper function to build the max heap recursively
    def build_max_heap(arr, n, i):
        if i < 0:
            return
        heapify_recursive(arr, n, i)
        build_max_heap(arr, n, i - 1)

    # Build the max heap
    build_max_heap(arr, n, n // 2 - 1)

    # Recursive function to sort the heap
    def sort_heap(arr, n):
        if n <= 1:
            return
        arr[0], arr[n - 1] = arr[n - 1], arr[0]  # Move max to the end
        heapify_recursive(arr, n - 1, 0)
        sort_heap(arr, n - 1)

    # Sort the heap
    sort_heap(arr, n)
    return arr

if __name__ == "__main__":
    # Example usage
    arr = [12, 11, 13, 5, 6, 7]
    print("Sorted array:", heap_sort_recursive(arr))

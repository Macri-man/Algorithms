def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1  # Index for smaller element

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort_iterative(arr):
    # Create an auxiliary stack
    stack = [(0, len(arr) - 1)]

    # Process the stack until it's empty
    while stack:
        low, high = stack.pop()

        if low < high:
            pi = partition(arr, low, high)

            # Push the subarrays onto the stack
            stack.append((low, pi - 1))
            stack.append((pi + 1, high))

    return arr

if __name__ == "__main__":
    # Example usage
    arr = [10, 7, 8, 9, 1, 5]
    print("Sorted array:", quick_sort_iterative(arr))

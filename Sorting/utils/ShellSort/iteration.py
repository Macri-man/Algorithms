def shell_sort_iterative(arr,capture):
    n = len(arr)
    gap = n // 2  # Start with an initial gap size

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            # Perform a gap-based insertion sort
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
            capture(arr)
        gap //= 2  # Reduce the gap size
       

    return arr

if __name__ == "__main__":

    # Example Usage
    arr = [12, 34, 54, 2, 3]
    print("Iterative Shell Sort:", shell_sort_iterative(arr))